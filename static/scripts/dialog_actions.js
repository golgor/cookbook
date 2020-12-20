// This file contains all scripts used to handle the dialogs, including opening, closing, input validation.
function addEventListeners(){
    $("#openTipDialog").click(function(event){
        Metro.dialog.open('#tipsDialogBox');
        $("#tipInputBox").focus();
    });

    $("#openIngredientDialog").click(function(event){
        Metro.dialog.open('#ingredientsDialogBox');
        $("#ingredientInputBox").focus();
    });

    $("#openRecipeStepDialog").click(function(event){
        Metro.dialog.open('#stepsDialogBox');
        $("#stepsInputBox").focus();
    });


    $("#addTipFromDialogBox").click(function(event){
        add_tip_step();
    });

    $("#addIngredientFromDialogBox").click(function(event){
        // Need to check if the ingredient is in the database before adding
        check_ingredient(
            success_callback=add_ingredient,
            failure_callback=handle_error
        );
    });

    $("#addRecipeStepFromDialogBox").click(function(event){
        add_recipe_step();
    });

    $("#tipInputBox").keyup(function(event){
        if (event.keyCode === 13) {
            add_tip_step();
        }
    });

    $("#ingredientInputBox").keyup(function(event){
        if (event.keyCode === 13) {
            check_ingredient(
                success_callback=add_ingredient,
                failure_callback=handle_error
            );
        }
        autoCompleteIngredients(this);
    });

    $("#stepsInputBox").keyup(function(event){
        if (event.keyCode === 13) {
            add_recipe_step();
        }
    });
}

// Autocomplete function for the input field in the #ingredientsDialogBox
function autoCompleteIngredients(inputField){
    if(inputField.value.length >= 1){
        let input_el = Metro.getPlugin("#ingredientInputBox",'input');
        $.get("/ingredients?q=" + inputField.value, function(ingredients){
            input_el.autocomplete = ingredients;
        })
    }
}

// Used to verify that an ingredient exists in the database just before adding it to the recipe.
function check_ingredient(success_callback, failure_callback){
    let ingredient_name = $("#ingredientInputBox").val();
    // Get request send to the backend to check if the ingredient exists in the database. The response is a Bool.
    $.ajax({
        method: "GET",
        url: "/ingredients/check?q=" + ingredient_name,
    }).then(function(response){
        // If successfully received response from the server
        if(response === true){
            // If ingredient exists
            success_callback();
        }
        else{
            // If the ingredient couldn't be found, show alert. Do not close the dialog.
            alert("Can't find the ingredient in the database, please double-check the name!");
        }
    }, function(response){
        // If there was no response received from the server.
        failure_callback();
    });
}

// Function to handle errors
function handle_error(){
    alert("Internal error!");
}