# Kafka commands
----------------

# to start Zookeeper
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties


# to start kafka server
.\bin\windows\kafka-server-start.bat .\config\server.properties

# to create a topic
.\bin\windoows\kafka-topics.sh --create --bootstrap-server localhost:9092 --repp;ication-factor 1 --partitions 1 --topic test

# to list a topic
.\bin\windows\kafka-toppics.sh --list --bootstrap-server localhost:9092

# for Console Producer
.\bin\windows\kafka-console-producer.sh --broker-list localhost:9092 --topic test

# for Console Consumer
.\bin\windows\kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
