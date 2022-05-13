// Run when the page is loaded
$(document).ready(function() {
    var filter_recipes = function(visible_class) {
        $(".recipe").each(function() {
            // If the recipe has the visible class, show it
            // else, set it to hidden
            if ($(this).hasClass(visible_class)) {
                $(this).show();
            }
            else {
                $(this).hide();
            }
        });
    };

    // Run when the select element with id tags is changed
    $("#tags").change(function() {
        console.log("Tags changed");
        
        // Print out all of the selected tags
        $("#tags option:selected").each(function() {
            console.log($(this).val());
            filter_recipes($(this).val());
        });
    });

    // Run when the select element with id ingredients is changed
    $("#ingredients").change(function() {
        console.log("Ingredients changed");

        // Print out all of the selected ingredients
        $("#ingredients option:selected").each(function() {
            console.log($(this).val());
            filter_recipes($(this).val());
        });
    });
});