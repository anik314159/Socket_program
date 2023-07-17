
echo "Server Started"
docker run -i  --rm --network=controller_net --name controller controller_cont & 
sleep 2s

gnome-terminal --window-with-profile=Profile0  -- bash -c "docker run -it --rm --network=controller_net client1cont" & 
gnome-terminal --window-with-profile=Profile0  -- bash -c "docker run -it --rm --network=controller_net client2cont" &
gnome-terminal --window-with-profile=Profile0  -- bash -c "docker run -it --rm --network=controller_net client3cont" &
