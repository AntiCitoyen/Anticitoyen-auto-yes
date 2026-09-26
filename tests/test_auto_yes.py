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
import subprocess
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

    def question(self, script, avant=None):
        t = Terminal([os.path.join(BIN, "auto-yes"), "/bin/bash", "-c", script])
        try:
            if avant:
                avant(t)
            return t.lire(10, b"RECU=")
        finally:
            self.journal = self.lire_journal(t)
            t.fermer()

    @staticmethod
    def lire_journal(t):
        chemin = os.path.join(t.maison, ".local", "state", "auto-yes", "journal.log")
        if not os.path.exists(chemin):
            return ""
        with open(chemin, encoding="utf-8") as f:
            return f.read()

    def test_menu_de_confirmation_recoit_1(self):
        sortie = self.question(
            'sleep 0.5; printf "Do you want to proceed?\\n  1. Yes\\n  2. No\\n"; read r; echo "RECU=$r"')
        self.assertIn("RECU=1", sortie)

    def test_phrase_seule_ne_declenche_rien(self):
        sortie = self.question(
            'sleep 0.5; printf "Do you want to proceed?\\n"; read -t 2 r; echo "RECU=[$r]"')
        self.assertIn("RECU=[]", sortie)

    def test_menu_qui_defile_est_ignore(self):
        # la question citée dans un texte qui continue de défiler n'est pas un menu qui attend
        sortie = self.question(
            'sleep 0.5; printf "Do you want to proceed?\\n  1. Yes\\n"; '
            'for i in $(seq 20); do echo ligne $i; sleep 0.05; done; read -t 2 r; echo "RECU=[$r]"')
        self.assertIn("RECU=[]", sortie)
        self.assertIn("ignoré:défilement", self.journal)

    def test_reponse_notee_au_journal(self):
        self.question('sleep 0.5; printf "Do you want to proceed?\\n  1. Yes\\n"; read r; echo "RECU=$r"')
        ligne = self.journal.strip().splitlines()[-1].split("\t")
        self.assertEqual(ligne[1], "réponse")
        self.assertEqual(ligne[2], "bash")
        self.assertTrue(ligne[3].endswith("1."), ligne[3])

    def test_pause_puis_reprise(self):
        def pause(t):
            dossier = os.path.join(t.maison, ".local", "state", "auto-yes")
            os.makedirs(dossier, exist_ok=True)
            open(os.path.join(dossier, "pause"), "w").close()
        sortie = self.question(
            'sleep 0.5; printf "Do you want to proceed?\\n  1. Yes\\n"; read -t 2 r; echo "RECU=[$r]"',
            avant=pause)
        self.assertIn("RECU=[]", sortie)
        self.assertIn("ignoré:pause", self.journal)

    def test_commandes_de_gestion(self):
        with tempfile.TemporaryDirectory() as etat:
            env = dict(os.environ, AUTO_YES_ETAT=etat, AUTO_YES_JOURNAL="")
            def lancer(*args):
                return subprocess.run([os.path.join(BIN, "auto-yes"), *args], env=env,
                                      capture_output=True, text=True, timeout=20).stdout
            self.assertIn("actif", lancer("--etat"))
            lancer("--pause")
            self.assertTrue(os.path.exists(os.path.join(etat, "pause")))
            self.assertIn("en pause", lancer("--etat"))
            lancer("--reprise")
            self.assertFalse(os.path.exists(os.path.join(etat, "pause")))


if __name__ == "__main__":
    unittest.main()
