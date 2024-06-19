<template>
  <div class="card-body">
    <h3>Connection status</h3>
    <p class="text-danger" v-if="!connected">Not connected!</p>
    <p class="text-success" v-if="connected">Connected!</p>
    <label>ROSBridge address</label>
    <br />
    <input type="text" v-model="rosbridge_address" />
    <br /><br />
    <button
      :disabled="loading"
      class="btn btn-danger"
      @click="disconnect"
      v-if="connected"
    >
      Disconnect!
    </button>
    <button :disabled="loading" class="btn btn-success" @click="connect" v-else>
      Connect!
    </button>
  </div>
</template>

<script>
import ROSLIB from "roslib";
export default {
  name: "RobotConfigComponent",

  data() {
    return {
      connected: false,
      ros: null,
      logs: [],
      loading: false,
      rosbridge_address: "wss://i-0f6f99b9ec098a68c.robotigniteacademy.com/b65609ba-59e1-45a4-9c07-2bfbc3257f58/rosbridge/",
      port: "9090",
      state: false,
      mapViewer: null,
      mapGridClient: null,
      interval: null,
    };
  },
  methods: {
    connect() {
      this.loading = true;
      this.ros = new ROSLIB.Ros({
        url: this.rosbridge_address
      });
      this.ros.on("connection", () => {
        console.log("Conectado a ROS");
        this.logs.unshift(`${new Date().toTimeString()} - ¡Conectado!`);
        this.connected = true;
        this.loading = false;
        //emito el eveto
        this.$emit("my-event", this.ros);
      });
      this.ros.on("error", (error) => {
        this.logs.unshift(`${new Date().toTimeString()} - Error: ${error}`);
        this.loading = false;
      });
      this.ros.on("close", () => {
        this.logs.unshift(`${new Date().toTimeString()} - ¡Desconectado!`);
        this.connected = false;
        this.loading = false;
        console.log("Desconectado");
      });
    },
    disconnect() {
      if (this.ros) {
        this.ros.close();
      }
    },
  },
};
</script>

<style scoped>
/* Add any styles specific to the config page here */
</style>
