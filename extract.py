__author__ = 'emrecelikten'

import json
import sys
import codecs

def load_hangouts_json(filename):
    with open(filename) as f:
        return json.load(f)


def find_user_id(data, person_name):
    for state in data['conversation_state']:
        conversation = state['conversation_state']['conversation']
        participants = conversation['participant_data']
        if len(participants) == 2:
            for participant in participants:
                if participant['fallback_name'] == person_name:
                    return participant['id']['gaia_id']

    return ''


def fetch_messages(data, user_id):
    messages = []
    for state in data['conversation_state']:
        conversation_state = state['conversation_state']
        conversation = conversation_state['conversation']
        participants = conversation['participant_data']
        if len(participants) == 2:
            for participant in participants:
                if participant['id']['gaia_id'] == user_id:
                    for event in conversation_state['event']:
                        sender = event['sender_id']['gaia_id']

                        if 'chat_message' in event:
                            content = event['chat_message']['message_content']
                            if 'segment' in content:
                                segments = content['segment']

                                for segment in segments:
                                    if 'text' in segment:
                                        message = segment['text'].strip()
                                        if len(message) != 0:
                                            messages.append((long(event['timestamp']), sender, message))

    messages.sort(key=lambda x: x[0])
    return messages


def write_to_file(messages, out_filename):
    with codecs.open(out_filename, 'w', encoding='utf8') as f:
        for message in messages:
            f.write(u"{0}\t{1}\t{2}\n".format(message[0], message[1], message[2]))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: <file> <person_name> <output_file>"
        exit()

    input_filename = sys.argv[1]
    person_name = sys.argv[2]
    output_filename = sys.argv[3]

    print "Searching for person: %s" % person_name

    data = load_hangouts_json(input_filename)
    user_id = find_user_id(data, person_name)

    print "User id for %s is %s." % (person_name, user_id)

    messages = fetch_messages(data, user_id)

    print "Found %d messages." % len(messages)

    write_to_file(messages, output_filename)