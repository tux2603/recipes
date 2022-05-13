// Run when the page is loaded
$(document).ready(function() {
    var filterRecipes = function(requiredClasses) {
        //If visible class is a string, make it an array
        if (typeof requiredClasses === 'string') {
            requiredClasses = [requiredClasses];
        }

        $(".recipe").each(function() {
            // If the recipe has all of the required classes, show it
            var hasAllClasses = true;
            var recipe = $(this);

            requiredClasses.forEach(function(requiredClass) {
                if (!recipe.hasClass(requiredClass)) {
                    hasAllClasses = false;
                }
            });
            
            if (hasAllClasses) {
                $(this).show();
            }

            else {
                $(this).hide();
            }
        });

        // Check to see if any of the recipe sections need to be hidden
        $(".recipe-section").each(function() {
            $(this).show();
            console.log($(this).find(".recipe:visible").length);
            if ($(this).find(".recipe:visible").length === 0) {
                $(this).hide();
            }
        });
    };

    var updateDisplayedRecipes = function() {
        // Silly hack so that if no tags or ingredients are selected, all recipes are displayed
        var required_classes = ['recipe'];

        $("#tags option:selected").each(function() {
            if ($(this).val() != "all") {
                required_classes.push($(this).val());
            }
        });

        $("#ingredients option:selected").each(function() {
            if ($(this).val() != "all") {
                required_classes.push($(this).val());
            }
        });

        filterRecipes(required_classes);
    };

    var showAllRecipes = function() {
        $(".recipe").show();
    };

    // Run when the select element with id tags is changed
    $("#tags").change(updateDisplayedRecipes);

    // Run when the select element with id ingredients is changed
    $("#ingredients").change(updateDisplayedRecipes);
});