// This file contains all scripts used to add/remove items in the lists

// Function to add ingredients to a list.
function add_ingredient(){
    Metro.dialog.close('#ingredientsDialogBox');

    name = get_text_and_clear("ingredientInputBox");
    amount = parseInt($("#amount_spinner").val());
    unit = $("#unit_selector").val();
    ingredient = {"name": name, "amount": amount, "unit": unit};

    element = create_list_item([{"label":name}, {"second_label":amount + unit}]);
    hidden_input = create_hidden_input(
        name="ingredient_input",
        value=JSON.stringify(ingredient)
    )
    element.appendChild(hidden_input);

    $("#ingredient_ul").append(element);
    
    // To clear: unit_selector (set to liter (l)), amount_spinner (0)
}

function add_prep_step(){
    text = get_text_and_clear("prepInputBox");

    element = create_list_item([{"label":text}]);
    val = {"text": text};
    hidden_input = create_hidden_input(
        name="prep_input",
        value=JSON.stringify(val)
    )
    element.appendChild(hidden_input);
    $("#prep_ul").append(element);
}

function add_recipe_step(){
    console.log("Adding recipe step!");

    text = get_text_and_clear("stepsInputBox");

    element = document.createElement("li");

    count = $("#recipeStepList")[0].childElementCount;
    heading = create_heading_tag(size="h4", step=count);

    content = document.createElement("p");
    content.textContent = text;

    val = {"text": text};

    hidden_input = create_hidden_input(
        name="recipe_steps_list",
        value=JSON.stringify(val)
    )

    element.appendChild(heading);
    element.appendChild(content);
    element.appendChild(hidden_input);

    $("#recipeStepList").append(element);
}

// Helper function to get the text and clear the field.
function get_text_and_clear(id){
    text = $("#" + id).val();
    $("#" + id).val("");
    return text;
}


function create_heading_tag(size="h1", step){
    steps_array = ["First", "Second", "Third", "Fourth", "Fift", "Sixth", "Seventh", "Eighth", "Nineth", "Tenth", "Eleventh"]
    heading = document.createElement(size);
    heading.innerHTML = steps_array[step] + " step";
    return heading;
}
