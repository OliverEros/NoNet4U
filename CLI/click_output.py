import click

#prints error message
def error_out(message):
    click.echo(click.style(message, fg='red'))
#prints normal message
def message_out(message):
    click.echo(click.style(message, fg='blue'))