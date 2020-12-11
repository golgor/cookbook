// This file contains all scripts used to add/remove items in the lists

// Function to add ingredients to a list.
function add_ingredient(){
    Metro.dialog.close('#ingredientsDialogBox');

    let name = get_text_and_clear("ingredientInputBox");
    let amount = parseInt($("#amount_spinner").val());
    let unit = $("#unit_selector").val();
    let ingredient = {"name": name, "amount": amount, "unit": unit};

    let element = create_list_item([{"label":name}, {"second_label":amount + unit}]);
    let hidden_input = create_hidden_input(
        name="ingredient_input",
        value=JSON.stringify(ingredient)
    )
    element.appendChild(hidden_input);

    $("#ingredient_ul").append(element);
    
    // To clear: unit_selector (set to liter (l)), amount_spinner (0)
}

function add_tip_step(){
    let text = get_text_and_clear("tipInputBox");

    let element = create_list_item([{"label":text}]);
    let val = {"text": text};
    let hidden_input = create_hidden_input(
        name="tip_input",
        value=JSON.stringify(val)
    )
    element.appendChild(hidden_input);
    $("#tip_ul").append(element);
}

function add_recipe_step(){
    let text = get_text_and_clear("stepsInputBox");

    let element = document.createElement("li");

    let count = $("#recipeStepList")[0].childElementCount;
    let heading = create_heading_tag(size="h4", step=count);

    let content = document.createElement("p");
    content.textContent = text;

    let val = {"text": text};

    let hidden_input = create_hidden_input(
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
    let text = $("#" + id).val();
    $("#" + id).val("");
    return text;
}


function create_heading_tag(size="h1", step){
    let steps_array = ["First", "Second", "Third", "Fourth", "Fift", "Sixth", "Seventh", "Eighth", "Nineth", "Tenth", "Eleventh"]
    let heading = document.createElement(size);
    heading.innerHTML = steps_array[step] + " step";
    return heading;
}
