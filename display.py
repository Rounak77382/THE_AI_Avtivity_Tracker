import ipywidgets as widgets
from IPython.display import display

# Define widgets with modern and formal styling
title = widgets.HTML(
    "<h2 style='color: #4CAF50; text-align: center;'>Process Productivity Analyzer</h2>"
)

instruction = widgets.HTML(
    "<p style='text-align: center;'>Analyze if a running process is directly productive for a software developer.<br>"
    "Enter the process title below and click 'Submit' to evaluate.</p>"
)

input_box = widgets.Text(
    value='',
    placeholder='e.g., Untitled - Opera',
    layout=widgets.Layout(width='50%', padding='10px'),
    style={'description_width': 'initial'}
)

submit_button = widgets.Button(
    description='Submit',
    button_style='info',  # Modern button style
    tooltip='Click to analyze the process',
    icon='check-circle'
)

output_box = widgets.Output(
    layout=widgets.Layout(
        border='2px solid #383838', 
        padding='10px', 
        width='auto',
        margin='20px auto'
    )
)

footer = widgets.HTML(
    "<p style='text-align: center; color: gray; font-size: 12px;'>Powered by Gemma 2 9b Model</p>"
)

# Arrange widgets in a vertical modern layout
ui_layout = widgets.VBox(
    [
        title,
        instruction,
        input_box,
        submit_button,
        output_box,
        footer
    ],
    layout=widgets.Layout(
        align_items='center',
        padding='20px',
        border='1px solid lightgray',
        border_radius='10px',
        box_shadow='0px 4px 8px rgba(0,0,0,0.1)'
    )
)

# Display the UI
display(ui_layout)

# Function to handle analysis
def analyze_process(_):
    with output_box:
        output_box.clear_output()
        
        alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

        ### Instruction:
        {}

        ### Input:
        {}

        ### Response:
        {}"""
        
        instruction = "I will provide a process title representing a currently running process on a computer. Your task is to analyze the process to determine if it is directly productive for a SOFTWARE DEVELOPER.  \nReturn your output as boolean, where it corresponds to the productivity status of the respective process. Do not include any additional text or explanation in your response."
        
        inputs = tokenizer(
            [
                alpaca_prompt.format(
                    instruction, 
                    input_box.value,  # input
                    ""  # output
                )
            ], 
            return_tensors="pt"
        ).to("cuda")

        outputs = model.generate(**inputs, max_new_tokens=64, use_cache=True)
        result = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        
        # Extracting only the response
        response_start = result.find("### Response:") + len("### Response:")
        response = result[response_start:].strip()
        
        # Change border color based on response
        if response.lower() == 'true':
            output_box.layout.border = '2px solid green'
        else:
            output_box.layout.border = '2px solid red'
        
        # Display the result
        output_box.clear_output()

        output_box.append_stdout(response)

# Attach the function to the submit button
submit_button.on_click(analyze_process)