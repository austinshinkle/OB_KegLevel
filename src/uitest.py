from datetime import datetime
from nicegui import run, ui, app
import random 

def test_function():
	return random.randint(1,100)
	
async def handle_click():
    result = await run.cpu_bound(compute_sum, 1, 2)
    ui.notify(f'Sum is {result}')
    
def compute_sum(a: int, b: int):
	return a + b
	
ui.image('../media/Ostentatious Brewing - Robot 2.jpeg').style("width: 150px")
ui.markdown("#Ostententatious Brewing!")
ui.markdown("##This is a subtitle")
	

with ui.splitter(value=50) as splitter:
	with splitter.before:
		label = ui.label()
		ui.button('shutdown', on_click=app.shutdown)
	with splitter.after:
		label2 = ui.label()
		ui.button('Random!', on_click=handle_click)
		
		


ui.timer(1.0, lambda: label.set_text(f'{datetime.now():%X}'))
ui.timer(2.0, lambda: label2.set_text(test_function()))


ui.run(reload=False)
