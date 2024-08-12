document.addEventListener("DOMContentLoaded", function() {
    var searchForm = document.getElementById("search-form");
    var allSujets = document.querySelectorAll(".sujets");

    searchForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Empêche l'envoi du formulaire par défaut

        var matiereValue = document.getElementById("input-matiere").value.trim().toLowerCase();
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
});