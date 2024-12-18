bc=`< /sys/class/power_supply/BAT0/capacity` # battery capacity
scaled=$((bc * 10))

_bs=`< /sys/class/power_supply/BAT0/status` # battery status

capacity_thresholds=(125 375 625 875 1000)
for i in "${!capacity_thresholds[@]}"; do
    if [ $scaled -le ${capacity_thresholds[$i]} ]; then
        battery_class=$i
        break
    fi
done

battery_discharge_icons=("" "" "" "" "")

case "$_bs" in
    "Charging") battery_icon="";;
    "Discharging") battery_icon="${battery_discharge_icons[$battery_class]}";;
    *) battery_icon="";;
esac

echo '{"capacity":'"$bc"',"icon":''"'"$battery_icon"'",''"class":'"$battery_class}"
