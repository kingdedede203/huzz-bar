print_audio_json() {
    case `pactl list sinks | sed -n 's/\sActive Port: //p'` in
        "analog-output-headphones") sink_icon="";;
        *) sink_icon="";;
    esac
    echo '{"sink-icon":''"'"$sink_icon"'","sink-volume":' \
            "$(pactl get-sink-volume @DEFAULT_SINK@ | awk -F'[/%]' '/Volume:/{print $2}')," \
            '"muted":false}'
}

# initial sink icon and volume
print_audio_json

pactl subscribe \
    | grep --line-buffered "Event 'change' on sink #" \
    | while read -r; do
    print_audio_json
done
