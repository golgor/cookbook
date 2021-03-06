// This file contains all scripts used to create the different elements used, mostly while adding to lists

function create_list_item(children, remove_button=true){
    // Creating a list item
    let element = document.createElement("li");

    children.forEach(child => {
        let class_name = Object.keys(child)[0];
        let text = Object.values(child)[0];
        element.appendChild(
            create_span(
                span_class = class_name,
                text = text
            )
        );
        if (remove_button === true){
            element.appendChild(
                create_remove_button()
            );
        }
    });

    return element;
}

function create_remove_button(){
    let remove_button = create_span("second-action fas fa-times fg-red");
    remove_button.onclick = function() { this.parentElement.remove() };
    return remove_button;
}


// Hidden input
function create_hidden_input(name, value){
    let input = document.createElement('input');
    input.type = "hidden";
    input.name = name;
    input.value = value;
    return input;
}

// Span
function create_span(span_class="", text=""){
    let span = document.createElement("span");
    if (span_class != ""){
        span.className = span_class;
    }
    if (text != ""){
        span.textContent = text;
    }
    return span;
}
