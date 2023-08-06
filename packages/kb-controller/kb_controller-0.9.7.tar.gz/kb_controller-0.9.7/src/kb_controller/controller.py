import serial
import os
from datetime import datetime
from kb_controller.helpers import kb_config, kb_central, microbit, event_poller

current_track_id = 0
department_id = 0
tracks_per_department = {}

def start():
    clear_console()
    print()
    print(f'  CONTROLLER STARTER OP {datetime.now()}')
    print('===================================================')
    print()

    # TODO: prompt for api_user/password on startup, and set this in kb_config
    # (and remove from the .ini file!!)

    microbit.initialize_connection()

    global current_track_id
    global department_id
    global tracks_per_department

    department_id = kb_central.get_department_id_from_token()
    tracks_per_department = kb_central.get_tracks()

    show_console_info()

    while True:

        if current_track_id > 0 and event_poller.thread is None:
            event_poller.start_thread(current_track_id)

        try:
            byteText = microbit.read_line()
            response = ''
            text = str(byteText, 'utf-8').strip()

            if not text == '':
                print('m:b <<< ' + text)

                if (text == 'quit'):
                    microbit.send_message('OK:QUIT')
                    break

                if (text.startswith('init:')):
                    track = text[5:]
                    if not track in tracks_per_department[department_id]['tracks']:
                        print(f'ERROR! Bane ID {track} findes ikke for afdeling {department_id}')
                        response = 'ERROR:INIT:INVALID-TRACK:' + track
                    else:
                        current_track_id = int(track)
                        response = 'OK:INIT:' + track
                        print_tracks()

                elif (current_track_id == 0):
                    print('Der er ikke tilknyttet en kuglebane til controlleren')
                    print('Brug kommandoen: "init:<<kuglebane-ID>>" for at tilknytte kuglebanen')
                    print("Dette kan du f.eks. programmere micro:bit'en til at gøre :-)")
                    print()
                    response = 'ERROR:NOT-INITIALIZED'

                elif (text == 'events'):
                    print()
                    print(f'Henter events for kuglebanen')
                    print('-----------------------------')
                    count = kb_central.get_number_of_events_for_track(current_track_id)
                    response = f'OK:EVENTS-TRACK:{current_track_id}:{count}'

                elif (text.startswith('send:')):
                    to_track = text[5:]
                    to_track_exists = False
                    for dep_id in tracks_per_department:
                        to_track_exists = to_track in tracks_per_department[dep_id]['tracks']
                        if to_track_exists:
                            break

                    if not to_track_exists:
                        print(f'ERROR! Bane ID {to_track} findes ikke!')
                        response = 'ERROR:START:INVALID-TRACK:' + to_track
                    else:
                        print()
                        print(
                            f'Sender START besked til "bane {to_track}"')
                        print('-------------------------------------')
                        kb_central.send_start_event(current_track_id, to_track)
                        response = 'OK:SEND:' + to_track

                elif (text.startswith('pop')):
                        print()
                        print(
                            f'"Popper" den ældste vent fra event-køen')
                        print('-------------------------------------')
                        events = kb_central.get_events_for_track(current_track_id)
                        if events is None or not 'events' in events:
                            response = 'ERROR:POP:INGEN-EVENTS'
                        else:
                            response = pop_event(events)

                else:
                    print('Ukendt kommando modtaget: ' + text)
                    response = 'ERROR:unknown-command'

            if not response=='':
                microbit.send_message(response)

        except serial.serialutil.SerialException as e:
            print()
            print("Der skete en fejl med den serielle forbindelse!")
            print(type(e))
            print(e)
            print(e.args)
            break

        except Exception as e:
            print()
            print("Der skete en fejl!")
            print(type(e))
            print(e)
            print(e.args)
            microbit.send_message('ERROR:Exception')

    microbit.close_connection()

    print()
    print(f'FARVEL! Controlleren lukker ned nu! {datetime.now()}')
    print()
    print('Venter på at tråden der poller kuglebane-centralen afslutter.')
    print(f'Der kan gå op til {kb_config.poll_interval_in_seconds} sekunder...')
    event_poller.signal_stop_thread()
    
def pop_event(events):
    # first event is always the oldest
    event_id_to_pop = list(events['events'])[0]
    event = events['events'][event_id_to_pop]

    command_id = event['command_id']
    from_department_id = event['from_department_id']
    from_track_id = event['from_track_id']
    from_track_name = event['from_track_name']

    print()
    print(f'Event ID: {event_id_to_pop}')
    print(f'  - kommando: {command_id}')
    print(f'  - modtaget fra afdeling: {from_department_id}')
    print(f'                kuglebane: {from_track_id} ("{from_track_name}")')
    print()

    kb_central.delete_event(event_id_to_pop)
    return f'OK:POP:{from_department_id}:{from_track_id}:{command_id}'

def clear_console():
    global department_id
    global tracks_per_department
    os.system('cls' if os.name == 'nt' else 'clear')

def show_console_info():
    print()
    print('============================================================')
    print('   M I C R O : B I T   S E R I A L   C O N T R O L L E R')
    print('============================================================')
    print(f'Kuglebane central........: {kb_config.kbc_host}')
    print(f'Controller for afdeling..: {department_id}')
    print('-----------------------------------------------------------')
    print()
    print('Kommandoer:')
    print()
    print('  init:<<kuglebane_id>>')
    print('     - fortæller hvilken kuglebane controlleren håndterer')
    print()
    print('  events')
    print('     - henter alle events for den kuglebane controlleren håndterer')
    print('       BEMÆRK: controlleren spørger automatisk efter disse events i')
    print('               det interval der er angivet i "polling_interval" i ')
    print('               kbc-config.ini filen')
    print()
    print('  pop')
    print('     - henter den ældste besked til den kuglebane controlleren håndterer')
    print("     - sender kommandoen fra beskeden til micro:bit'en")
    print("     - sletter beskeden fra kuglebane centralen")
    print()
    print('  send:<<to_track_id>>')
    print('     - sender en besked til en anden kuglebane om at starte kuglen')
    print()
    print('  quit')
    print('     - Afbryder controlleren')
    print()
    print('-----------------------------------------------------------')
    print()

def print_tracks():
    global current_track_id
    global department_id
    global tracks_per_department

    print()
    print('-----------------------------------------------------------')
    print('Tilgængelige kuglebaner:')
    print()
    print(f'  {department_id} (egen afdeling):')
    print('  -------------------------------------')
    own_tracks = tracks_per_department[department_id]['tracks']
    for track_id in own_tracks:
        is_controlled_track = (int(track_id) == current_track_id)
        print(f"    {track_id} - {own_tracks[track_id]}    {'[CONTROLLER]' if is_controlled_track else ''}")
    print('  -------------------------------------')

    for dep_id in tracks_per_department:
        if not dep_id == department_id:
            print()
            print(f'  {dep_id}:')
            tracks = tracks_per_department[dep_id]['tracks']
            for track_id in tracks:
                print(f"    {track_id} - {tracks[track_id]}")
    print('-----------------------------------------------------------')
    print()


if __name__ == '__main__':
    start()