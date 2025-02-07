var count = 1;

function inputToCheckbox(tagInput, tagCheckbox) {
    var inputValue = document.getElementById(tagInput);
    var checkboxValue  = document.getElementById(tagCheckbox);
    checkboxValue.value = inputValue.value;
};

function addAnswer(tagContainerAnswers, qAnswerVariant, qRightAnswer) {
    var input = document.createElement('input');
    input.type = 'text';
    input.name = qAnswerVariant;
    input.value = "";
    input.id = qAnswerVariant + count;
    input.className = 'form-control';
    var checkbox = document.createElement('input');
    checkbox.className = 'form-check-input mt-0';
    checkbox.type = 'checkbox';
    checkbox.name = qRightAnswer;
    checkbox.id = qRightAnswer + count;
    checkbox.value = "";
    input.onchange = function() {inputToCheckbox(input.id, checkbox.id);};
    var inputGroup = document.createElement('div');
    inputGroup.className = 'input-group';
    var inputGroupText = document.createElement('div');
    inputGroupText.className = 'input-group-text';
    var container = document.getElementById(tagContainerAnswers);
    var br = document.createElement('br');
    container.appendChild(inputGroup);
    inputGroup.appendChild(inputGroupText);
    inputGroupText.appendChild(checkbox);
    inputGroup.appendChild(input)
    container.appendChild(br);
    count++;
}


