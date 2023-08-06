import asyncio

import click
import pyaudio
from rich.prompt import Prompt
from rich.table import Table

from voice_bot_demo.console import console
from voice_bot_demo.speech_text.assembly import AssemblySpeechText
from voice_bot_demo.speech_text.whisper import WhisperSpeechText
from voice_bot_demo.text_speech.gpt_pyttsx3 import GPT_PYTTSX3TextSpeech


def get_input_devices(p):
    device_list = []
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info["maxInputChannels"] > 0:
            device_list.append(device_info)
    return device_list


def get_input_device_by_name(p, device_name):
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info["name"] == device_name and device_info["maxInputChannels"] > 0:
            return device_info
    return None


@click.group()
@click.version_option()
def cli():
    "AI conversational bot."


@cli.command(name="start")
@click.option(
    "-d",
    "--device",
    type=str,
    default=None,
    help="Input device name. If not provided, the user will be prompted to choose an input device.",
)
@click.option(
    "-stm",
    "--speech-text-model",
    type=click.Choice(["assembly", "whisper"], case_sensitive=False),
    help="Speech to text model. If not provided, the user will be prompted to choose a model.",
    show_default=True,
)
def start(device: str, speech_text_model: str):
    p = pyaudio.PyAudio()

    if device is None:
        device_list = get_input_devices(p)
        table = Table()
        table.add_column("ID")
        table.add_column("Name")

        for i, dev in enumerate(device_list):
            table.add_row(str(i), dev["name"])

        console.print(table)
        device_index = Prompt.ask(
            "Please choose an input device by entering its ID",
            choices=[str(i) for i in range(len(device_list))],
        )
        chosen_device = device_list[int(device_index)]
    else:
        chosen_device = get_input_device_by_name(p, device)
        if chosen_device is None:
            click.echo(f"Error: Device '{device}' not found among input devices.")
            return

    click.echo(f"Using device: {chosen_device['name']}.")

    if speech_text_model is None:
        speech_text_model = Prompt.ask(
            "Please choose a speech to text model",
            choices=["assembly", "whisper"],
            default="assembly",
        )

    click.echo(f"Using model: {speech_text_model}.")

    console.print("[bold blue]Started. You may not start speaking.[/bold blue]")

    text_speech = GPT_PYTTSX3TextSpeech()
    if speech_text_model.lower() == "assembly":
        speech_text = AssemblySpeechText(
            chosen_device["index"], process_sentence=text_speech.process_sentence
        )
    else:
        speech_text = WhisperSpeechText(
            device_index=chosen_device["index"],
            process_sentence=text_speech.process_sentence,
        )
    asyncio.run(speech_text.run())


if __name__ == "__main__":
    cli()
