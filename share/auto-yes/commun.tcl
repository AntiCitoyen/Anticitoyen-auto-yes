# commun.tcl : code partagé par auto-yes et auto-yes-shell (chargé par `source`).
#
# Variables d'environnement :
#   AUTO_YES_PATTERNS  fichier de motifs (défaut /etc/auto-yes/patterns.conf)
#   AUTO_YES_CALME     silence exigé après le menu avant de répondre, en ms (défaut 300, 0 = aucun)
#   AUTO_YES_JOURNAL   fichier journal (défaut $XDG_STATE_HOME/auto-yes/journal.log, vide = pas de journal)
#   AUTO_YES_ETAT      dossier d'état : drapeau de pause (défaut $XDG_STATE_HOME/auto-yes)

namespace eval auto_yes {
    variable motif_defaut {(?i)do you want to proceed\??[^\n]*\n\s*1\.}
    variable sid ""
    variable pts ""

    variable etat
    if {[info exists ::env(AUTO_YES_ETAT)] && $::env(AUTO_YES_ETAT) ne ""} {
        set etat $::env(AUTO_YES_ETAT)
    } elseif {[info exists ::env(XDG_STATE_HOME)] && $::env(XDG_STATE_HOME) ne ""} {
        set etat [file join $::env(XDG_STATE_HOME) auto-yes]
    } else {
        set etat [file join $::env(HOME) .local state auto-yes]
    }
    variable journal [file join $etat journal.log]
    if {[info exists ::env(AUTO_YES_JOURNAL)]} { set journal $::env(AUTO_YES_JOURNAL) }
    variable calme 300
    if {[info exists ::env(AUTO_YES_CALME)] && [string is integer -strict $::env(AUTO_YES_CALME)]} {
        set calme $::env(AUTO_YES_CALME)
    }
}

proc auto_yes::drapeau_pause {} {
    variable etat
    return [file join $etat pause]
}

proc auto_yes::motifs {} {
    variable motif_defaut
    set fichier "/etc/auto-yes/patterns.conf"
    if {[info exists ::env(AUTO_YES_PATTERNS)]} { set fichier $::env(AUTO_YES_PATTERNS) }
    set motifs {}
    if {[file exists $fichier]} {
        set f [open $fichier r]
        while {[gets $f ligne] >= 0} {
            set ligne [string trim $ligne]
            if {$ligne eq "" || [string index $ligne 0] eq "#"} { continue }
            lappend motifs $ligne
        }
        close $f
    }
    if {[llength $motifs] == 0} { lappend motifs $motif_defaut }
    return $motifs
}

# Arguments de `interact` : chaque motif, appliqué à la sortie du programme, appelle repondre.
proc auto_yes::actions {} {
    set actions {}
    foreach m [motifs] {
        lappend actions -o -nobuffer -re $m {auto_yes::repondre $interact_out(0,string)}
    }
    return $actions
}

# À appeler juste après `spawn` : retient le processus et relaie les
# redimensionnements de la fenêtre (sans quoi le programme garde la taille du
# démarrage et l'édition des longues lignes se décale).
proc auto_yes::apres_spawn {} {
    variable sid
    variable pts
    upvar #0 spawn_id spawn_id spawn_out spawn_out
    set sid $spawn_id
    set pts $spawn_out(slave,name)
    trap {
        set taille [stty size]
        stty rows [lindex $taille 0] columns [lindex $taille 1] < $::auto_yes::pts
        catch {exec kill -WINCH [exp_pid -i $::auto_yes::sid]}
    } WINCH
}

proc auto_yes::premier_plan {} {
    variable pts
    set commande "?"
    catch {
        foreach ligne [split [exec ps -o stat=,comm= -t [string range $pts 5 end]] "\n"] {
            if {[string match *+* [lindex $ligne 0]]} { set commande [lrange $ligne 1 end] }
        }
    }
    return $commande
}

proc auto_yes::noter {issue texte commande} {
    variable journal
    if {$journal eq ""} { return }
    regsub -all {\x1b\[[0-9;?]*[ -/]*[@-~]} $texte "" texte
    regsub -all {[\x00-\x1f\x7f]+} $texte " " texte
    set texte [string range [string trim $texte] 0 159]
    catch {
        file mkdir [file dirname $journal]
        set f [open $journal a]
        puts $f "[clock format [clock seconds] -format {%Y-%m-%d %H:%M:%S}]\t$issue\t$commande\t$texte"
        close $f
    }
}

# Motif reconnu : répond « 1 » + Entrée, sauf en pause, ou si l'écran ne reste
# pas calme (un texte qui défile et cite la question n'est pas un menu qui attend).
proc auto_yes::repondre {texte} {
    variable sid
    variable calme
    # lu avant l'envoi : une fois « 1 » reçu, le programme peut déjà s'être terminé
    set commande [premier_plan]
    if {[file exists [drapeau_pause]]} {
        noter "ignoré:pause" $texte $commande
        return
    }
    if {$calme > 0} {
        # la fin du menu (« 2. No »…) arrive souvent dans la même rafale : elle ne compte pas
        expect -i $sid -timeout 0 -re {.+} {} timeout {} eof {}
        after $calme
        set suite 0
        expect -i $sid -timeout 0 -re {.+} { set suite 1 } timeout {} eof {}
        if {$suite} {
            noter "ignoré:défilement" $texte $commande
            return
        }
    }
    send -i $sid -- "1\r"
    noter "réponse" $texte $commande
}

# Options de gestion communes : --pause, --reprise, --etat, --journal [N].
# Retourne 1 si l'option a été traitée.
proc auto_yes::gerer {argv} {
    variable journal
    set drapeau [drapeau_pause]
    switch -- [lindex $argv 0] {
        --pause {
            file mkdir [file dirname $drapeau]
            close [open $drapeau w]
            puts "auto-yes en pause dans tous les terminaux (reprise : auto-yes --reprise)."
        }
        --reprise {
            file delete -- $drapeau
            puts "auto-yes actif."
        }
        --etat {
            if {[file exists $drapeau]} { puts "en pause" } else { puts "actif" }
            if {$journal eq ""} { puts "journal : désactivé" } else { puts "journal : $journal" }
        }
        --journal {
            set n [lindex $argv 1]
            if {![string is integer -strict $n]} { set n 20 }
            if {$journal eq "" || ![file exists $journal]} {
                puts "journal vide."
            } else {
                set f [open $journal r]
                set lignes [split [string trimright [read $f] "\n"] "\n"]
                close $f
                puts [join [lrange $lignes end-[expr {$n - 1}] end] "\n"]
            }
        }
        default { return 0 }
    }
    return 1
}

