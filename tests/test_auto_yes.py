"""Essais d'auto-yes et d'auto-yes-shell dans un pseudo-terminal.

Lancement : python3 -m unittest discover -s tests -v   (expect requis)
"""
import fcntl
import os
import pty
import select
import shutil
import signal
import struct
import tempfile
import termios
import time
import unittest

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(DEPOT, "bin")
MOTIFS = os.path.join(DEPOT, "etc", "patterns.conf")


def taille(fd, lignes, colonnes):
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", lignes, colonnes, 0, 0))


class Terminal:
    def __init__(self, argv):
        self.maison = tempfile.mkdtemp()
        env = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": self.maison,
            "SHELL": "/bin/bash",
            "TERM": "xterm",
            "PS1": "P$ ",
            "AUTO_YES_PATTERNS": MOTIFS,
        }
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            os.execve(argv[0], argv, env)
        taille(self.fd, 24, 80)

    def lire(self, duree=1.5, attendu=None):
        sortie = b""
        fin = time.time() + duree
        while time.time() < fin:
            prets, _, _ = select.select([self.fd], [], [], 0.1)
            if prets:
                try:
                    sortie += os.read(self.fd, 4096)
                except OSError:
                    break
                if attendu and attendu in sortie:
                    break
        return sortie.decode(errors="replace")

    def ecrire(self, texte):
        os.write(self.fd, texte.encode())

    def fermer(self):
        try:
            os.kill(self.pid, signal.SIGKILL)
            os.waitpid(self.pid, 0)
        except (ProcessLookupError, ChildProcessError):
            pass
        os.close(self.fd)
        shutil.rmtree(self.maison, ignore_errors=True)


@unittest.skipUnless(shutil.which("expect"), "expect absent")
class EssaisAutoYes(unittest.TestCase):
    def verifier_redimensionnement(self, argv):
        t = Terminal(argv)
        try:
            debut = t.lire(5, b"P$ ")
            taille(t.fd, 40, 200)
            os.kill(t.pid, signal.SIGWINCH)
            # le relais passe par stty (un processus) : sur une machine chargée, il tarde
            sortie = ""
            for _ in range(10):
                t.ecrire("echo TAILLE=$(stty size </dev/tty):$COLUMNS\r")
                sortie += t.lire(1, b"200:200")
                if "TAILLE=40 200:200" in sortie:
                    break
            etat = os.waitpid(t.pid, os.WNOHANG)
            self.assertIn("TAILLE=40 200:200", sortie,
                          f"début={debut[-200:]!r} état={etat}")
        finally:
            t.fermer()

    def test_shell_suit_la_taille_de_la_fenetre(self):
        self.verifier_redimensionnement([os.path.join(BIN, "auto-yes-shell")])

    def test_commande_suit_la_taille_de_la_fenetre(self):
        self.verifier_redimensionnement(
            [os.path.join(BIN, "auto-yes"), "/bin/bash", "--norc", "--noprofile", "-i"])

    def question(self, script):
        t = Terminal([os.path.join(BIN, "auto-yes"), "/bin/bash", "-c", script])
        try:
            return t.lire(10, b"RECU=")
        finally:
            t.fermer()

    def test_menu_de_confirmation_recoit_1(self):
        sortie = self.question(
            'sleep 0.5; printf "Do you want to proceed?\\n  1. Yes\\n  2. No\\n"; read r; echo "RECU=$r"')
        self.assertIn("RECU=1", sortie)

    def test_phrase_seule_ne_declenche_rien(self):
        sortie = self.question(
            'sleep 0.5; printf "Do you want to proceed?\\n"; read -t 2 r; echo "RECU=[$r]"')
        self.assertIn("RECU=[]", sortie)


if __name__ == "__main__":
    unittest.main()
