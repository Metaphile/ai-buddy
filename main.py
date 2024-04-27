from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

from transformers import AutoTokenizer, AutoModelForCausalLM

# pseudo code
# start with neutral expression
# await user input via terminal
# on input, select appropriate facial expression via LLM
# update display

# make the LLM come up with its own emoticons
# make the LLM come up with its own ASCII art animations

def get_llm_response():
    model_id = "CohereForAI/c4ai-command-r-plus"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)

    # Format message with the command-r-plus chat template
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    input_ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
    ## <BOS_TOKEN><|START_OF_TURN_TOKEN|><|USER_TOKEN|>Hello, how are you?<|END_OF_TURN_TOKEN|><|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>

    gen_tokens = model.generate(
        input_ids, 
        max_new_tokens=100, 
        do_sample=True, 
        temperature=0.3,
        )

    gen_text = tokenizer.decode(gen_tokens[0])
    return gen_text

def set_up_lcd():
    # it might be possible to define custom characters
    # https://lastminuteengineers.com/arduino-1602-character-lcd-tutorial/
    turn_on_backlight()
    set_columns_lines()

def turn_on_backlight():
    mcp.output(3, 1)

def set_columns_lines():
    lcd.begin(16, 2)
      
def destroy():
    lcd.clear()

def display_face():
    set_up_lcd()
    lcd.setCursor(0, 0)
    response = get_llm_response()
    lcd.message(response)

PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        display_face()
    except KeyboardInterrupt:
        destroy()
