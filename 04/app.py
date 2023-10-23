import googlemaps
import os
#GM_TOKEN=os.environ.get("GM_TOKEN") # Get Google Maps Token Here:  https://console.cloud.google.com/google/maps-apis/

from datetime import datetime

# googlemaps_TOKEN = os.environ.get("googlemaps_TOKEN")
# gmaps = googlemaps.Client(key=googlemaps_TOKEN)
gmaps = googlemaps.Client(key='AIzaSyDybq2mxujekZVivmr03Y5-GGHXesn4TLI')


def GetMapInfo(inputText):
    #geocode_result = gmaps.geocode('640 Jackson Street, St. Paul, MN 55101')
    geocode_result = gmaps.geocode(inputText)
    
    geo_address = geocode_result[0]['formatted_address']
    geo_directions = geocode_result[0]['geometry']['location']
    geo_geocode = geocode_result[0]['geometry']['location_type']
    
    lat = geo_directions['lat']
    lng = geo_directions['lng']
    
    reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
    
    now = datetime.now()
    directions_result = gmaps.directions("Sydney Town Hall","Parramatta, NSW",mode="transit", departure_time=now)
    #addressvalidation_result =  gmaps.addressvalidation(['1600 Amphitheatre Pk'], regionCode='US', locality='Mountain View', enableUspsCass=True)

    #return geocode_result, reverse_geocode_result, directions_result, addressvalidation_result
    #return geo_address, geo_directions, geo_geocode, reverse_geocode_result, directions_result, addressvalidation_result
    return geo_address, geo_directions, geo_geocode

from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch
import gradio as gr
from datasets import load_dataset

# PersistDataset -----
import os
import csv
from gradio import inputs, outputs
import huggingface_hub
from huggingface_hub import Repository, hf_hub_download, upload_file
from datetime import datetime

#fastapi is where its at:  share your app, share your api
import fastapi

from typing import List, Dict
import httpx
import pandas as pd
import datasets as ds

UseMemory=True
HF_TOKEN=os.environ.get("HF_TOKEN")

def SaveResult(text, outputfileName):
    basedir = os.path.dirname(__file__)
    savePath = outputfileName
    print("Saving: " + text + " to " + savePath)
    from os.path import exists
    file_exists = exists(savePath)
    if file_exists:
        with open(outputfileName, "a") as f: #append
            f.write(str(text.replace("\n","  ")))
            f.write('\n')
    else:
        with open(outputfileName, "w") as f: #write
            f.write(str("time, message, text\n")) # one time only to get column headers for CSV file
            f.write(str(text.replace("\n","  ")))
            f.write('\n')
    return

    
def store_message(name: str, message: str, outputfileName: str):
    basedir = os.path.dirname(__file__)
    savePath = outputfileName
    
    # if file doesnt exist, create it with labels
    from os.path import exists
    file_exists = exists(savePath)
    
    if (file_exists==False):
        with open(savePath, "w") as f: #write
            f.write(str("time, message, text\n")) # one time only to get column headers for CSV file
            if name and message:
                writer = csv.DictWriter(f, fieldnames=["time", "message", "name"])
                writer.writerow(
                    {"time": str(datetime.now()), "message": message.strip(), "name": name.strip()  }
                )
        df = pd.read_csv(savePath)
        df = df.sort_values(df.columns[0],ascending=False)
    else:
        if name and message:
            with open(savePath, "a") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=[ "time", "message", "name", ])
                writer.writerow(
                    {"time": str(datetime.now()), "message": message.strip(), "name": name.strip()  }
                )
        df = pd.read_csv(savePath)
        df = df.sort_values(df.columns[0],ascending=False)
    return df

mname = "facebook/blenderbot-400M-distill"
model = BlenderbotForConditionalGeneration.from_pretrained(mname)
tokenizer = BlenderbotTokenizer.from_pretrained(mname)

def take_last_tokens(inputs, note_history, history):
    if inputs['input_ids'].shape[1] > 128:
        inputs['input_ids'] = torch.tensor([inputs['input_ids'][0][-128:].tolist()])
        inputs['attention_mask'] = torch.tensor([inputs['attention_mask'][0][-128:].tolist()])
        note_history = ['</s> <s>'.join(note_history[0].split('</s> <s>')[2:])]
        history = history[1:]
    return inputs, note_history, history
    
def add_note_to_history(note, note_history):# good example of non async since we wait around til we know it went okay.
    note_history.append(note)
    note_history = '</s> <s>'.join(note_history)
    return [note_history]

title = "💬ChatBack🧠💾"
description = """Chatbot With persistent memory dataset allowing multiagent system AI to access a shared dataset as memory pool with stored interactions. 
 Current Best SOTA Chatbot:  https://huggingface.co/facebook/blenderbot-400M-distill?text=Hey+my+name+is+ChatBack%21+Are+you+ready+to+rock%3F  """

def get_base(filename): 
        basedir = os.path.dirname(__file__)
        print(basedir)
        #loadPath = basedir + "\\" + filename # works on windows
        loadPath = basedir + filename # works on ubuntu
        print(loadPath)
        return loadPath
    
def chat(message, history):
    history = history or []
    if history: 
        history_useful = ['</s> <s>'.join([str(a[0])+'</s> <s>'+str(a[1]) for a in history])]
    else:
        history_useful = []
        
    history_useful = add_note_to_history(message, history_useful)
    inputs = tokenizer(history_useful, return_tensors="pt")
    inputs, history_useful, history = take_last_tokens(inputs, history_useful, history)
    reply_ids = model.generate(**inputs)
    response = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
    history_useful = add_note_to_history(response, history_useful)
    list_history = history_useful[0].split('</s> <s>')
    history.append((list_history[-2], list_history[-1]))  
    
    df=pd.DataFrame()
    
    if UseMemory: 
        #outputfileName = 'ChatbotMemory.csv'
        outputfileName = 'ChatbotMemory3.csv' # Test first time file create
        df = store_message(message, response, outputfileName) # Save to dataset
        basedir = get_base(outputfileName)
        
    return history, df, basedir




with gr.Blocks() as demo:
  gr.Markdown("<h1><center>🍰 AI Google Maps Demonstration🎨</center></h1>")
  
  with gr.Row():
    t1 = gr.Textbox(lines=1, default="", label="Chat Text:")
    b1 = gr.Button("Respond and Retrieve Messages")
    b2 = gr.Button("Get Map Information")
    
  with gr.Row(): # inputs and buttons
    s1 = gr.State([])
    df1 = gr.Dataframe(wrap=True, max_rows=1000, overflow_row_behaviour= "paginate")
  with gr.Row(): # inputs and buttons
    file = gr.File(label="File")
    s2 = gr.Markdown()
  with gr.Row():
    df21 = gr.Textbox(lines=4, default="", label="Geocode1:")
    df22 = gr.Textbox(lines=4, default="", label="Geocode2:")
    df23 = gr.Textbox(lines=4, default="", label="Geocode3:")
    df3 = gr.Dataframe(wrap=True, max_rows=1000, overflow_row_behaviour= "paginate")
    df4 = gr.Dataframe(wrap=True, max_rows=1000, overflow_row_behaviour= "paginate")
  b1.click(fn=chat, inputs=[t1, s1], outputs=[s1, df1, file]) 
  b2.click(fn=GetMapInfo, inputs=[t1], outputs=[df21, df22, df23]) 
    
demo.launch(debug=True, show_error=True)
