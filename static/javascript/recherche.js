document.addEventListener("DOMContentLoaded", function() {
    var searchForm = document.getElementById("search-form");
    var allSujets = document.querySelectorAll(".sujets");
    var matiereInput = document.getElementById("input-matiere");
    var anneeInput = document.getElementById("input-annee");

    searchForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Empêche l'envoi du formulaire par défaut

        var matiereValue = document.getElementById("input-matiere").value.trim().toLowerCase();// la methode trim supprime les blancs en debut et fin de chaine
        var anneeValue = document.getElementById("input-annee").value.trim();

        allSujets.forEach(function(sujet) {
            sujet.style.display = "none"; // Masque tous les sujets au début de chaque recherche
        });

        if (matiereValue && anneeValue) {
            allSujets.forEach(function(sujet) {
                var sujetMatiere = sujet.getAttribute("data-matiere").toLowerCase();
                var sujetAnnee = sujet.getAttribute("data-annee");

                if (sujetMatiere === matiereValue && sujetAnnee === anneeValue) {
                    sujet.style.display = "block"; // Affiche les sujets correspondants
                }
            });
        } else if (matiereValue) {
            allSujets.forEach(function(sujet) {
                var sujetMatiere = sujet.getAttribute("data-matiere").toLowerCase();

                if (sujetMatiere === matiereValue) {
                    sujet.style.display = "block"; // Affiche les sujets correspondants par matière
                }
            });
        } else if (anneeValue) {
            allSujets.forEach(function(sujet) {
                var sujetAnnee = sujet.getAttribute("data-annee");

                if (sujetAnnee === anneeValue) {
                    sujet.style.display = "block"; // Affiche les sujets correspondants par année
                }
            });
        } else {
            allSujets.forEach(function(sujet) {
                sujet.style.display = "block"; // Affiche tous les sujets si aucun filtre n'est appliqué
            });
        }
    });

    // Recherche instantanée pour la matière
    matiereInput.addEventListener("input", function() {
        var matiereValue = document.getElementById("input-matiere").value.trim().toLowerCase();
        allSujets.forEach(function(sujet) {
            var sujetMatiere = sujet.getAttribute("data-matiere").toLowerCase();
            sujet.style.display = sujetMatiere.includes(matiereValue)? "block" : "none"; // Affiche les sujets correspondants à la matière
            if (sujetMatiere === matiereValue) {
                sujet.scrollIntoView({ behavior: "smooth" }); // Scroll vers le premier sujet correspondant
            }
        });
    });


    // Recherche instantanée pour l'année
    anneeInput.addEventListener("input", function() {
        var anneeValue = document.getElementById("input-annee").value.trim();
        allSujets.forEach(function(sujet) {
            var sujetAnnee = sujet.getAttribute("data-annee");
            sujet.style.display = sujetAnnee.includes(anneeValue)? "block" : "none"; // Affiche les sujets correspondants à l'année
            if (sujetAnnee === anneeValue) {
                sujet.scrollIntoView({ behavior: "smooth" }); // Scroll vers le premier sujet correspondant
            }
        });
    });
});