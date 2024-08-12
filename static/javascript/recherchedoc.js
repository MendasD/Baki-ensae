document.addEventListener("DOMContentLoaded", function() {
    var searchForm = document.getElementById("search-form");
    var allSujets = document.querySelectorAll(".documents");
    var matiereInput = document.getElementById("input-matiere");
    var classeInput = document.getElementById("input-classe");
    var auteurInput = document.getElementById("input-auteur");

    searchForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Empêche l'envoi du formulaire par défaut

        var matiereValue = document.getElementById("input-matiere").value.trim().toLowerCase();
        var classeValue = document.getElementById("input-classe").value.trim();
        var auteurValue = document.getElementById("input-auteur").value.trim();

        allSujets.forEach(function(sujet) {
            sujet.style.display = "none"; // Masque tous les documents au début de chaque recherche
        });

        if (matiereValue && anneeValue && auteurValue) {
            allSujets.forEach(function(sujet) {
                var sujetMatiere = sujet.getAttribute("data-matiere").toLowerCase();
                var sujetClasse = sujet.getAttribute("data-classe").toLowerCase();
                var sujetAuteur = sujet.getAttribute("data-auteur").toLowerCase();

                if (sujetMatiere === matiereValue && sujetClasse === classeValue && sujetAuteur === auteurValue) {
                    sujet.style.display = "block"; // Affiche les documents correspondants
                }
            });
        } else if (matiereValue && classeValue) {
            allSujets.forEach(function(sujet) {
                var sujetMatiere = sujet.getAttribute("data-matiere").toLowerCase();
                var sujetClasse = sujet.getAttribute("data-classe").toLowerCase();

                if (sujetMatiere === matiereValue && sujetClasse === classeValue) {
                    sujet.style.display = "block"; // Affiche les sujets correspondants par matière
                }
            });
        } else if (matiereValue && auteurValue) {
            allSujets.forEach(function(sujet) {
                var sujetAuteur = sujet.getAttribute("data-auteur").toLowerCase(); 
                var sujetMatiere = sujet.getAttribute("data-matiere").toLowerCase();

                if (sujetAuteur === auteurValue && sujetMatiere === matiereValue) {
                    sujet.style.display = "block"; // Affiche les sujets correspondants par année
                }
            });
        } else if (classeValue && auteurValue ){
            allSujets.forEach(function(sujet) {
                var sujetAuteur = sujet.getAttribute("data-auteur").toLowerCase();
                var sujetClasse = sujet.getAttribute("data-classe").toLowerCase();
                
                if (sujetAuteur === auteurValue && sujetClasse === classeValue) {
                    sujet.style.display = "block"; // Affiche les sujets correspondants par année
                }
            });
        } else if (matiereValue) {
            allSujets.forEach(function(sujet) {
                var sujetMatiere = sujet.getAttribute("data-matiere").toLowerCase();
                sujet.style.display = sujetMatiere === matiereValue? "block" : "none"; // Affiche les sujets correspondants à la matière
            });
        } else if (classeValue) {
            allSujets.forEach(function(sujet) {
                var sujetClasse = sujet.getAttribute("data-classe").toLowerCase();
                sujet.style.display = sujetClasse === classeValue? "block" : "none"; // Affiche les sujets correspondants à la classe
            });
        } else if (auteurValue) {
            allSujets.forEach(function(sujet) {
                var sujetAuteur = sujet.getAttribute("data-auteur").toLowerCase();
                sujet.style.display = sujetAuteur === auteurValue? "block" : "none"; // Affiche les sujets correspondants à l'auteur
            });
        } else {
            allSujets.forEach(function(sujet) {  // Masque tous les documents si aucun filtre n'est appliqué
                sujet.style.display = "none";
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


    // Recherche instantanée pour la classe
    classeInput.addEventListener("input", function() {
        var classeValue = document.getElementById("input-classe").value.trim().toLowerCase();
        allSujets.forEach(function(sujet) {
            var sujetClasse = sujet.getAttribute("data-classe").toLowerCase();
            sujet.style.display = sujetClasse.includes(classeValue)? "block" : "none"; // Affiche les sujets correspondants à l'année
            if (sujetClasse === classeValue) {
                sujet.scrollIntoView({ behavior: "smooth" }); // Scroll vers le premier sujet correspondant
            }
        });
    });


    // Recherche instantanée pour l'auteur
    auteurInput.addEventListener("input", function() {
        var auteurValue = document.getElementById("input-auteur").value.trim().toLowerCase();
        allSujets.forEach(function(sujet) {
            var sujetAuteur = sujet.getAttribute("data-auteur").toLowerCase();
            sujet.style.display = sujetAuteur.includes(auteurValue)? "block" : "none"; // Affiche les sujets correspondants à l'auteur
            if (sujetAuteur === auteurValue) {
                sujet.scrollIntoView({ behavior: "smooth" }); // Scroll vers le premier sujet correspondant
            }
        });
    });
});