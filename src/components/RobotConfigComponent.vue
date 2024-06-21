<template>
  <div class="card mb-3 w-100 p-3 shadow-sm">
    <div class="card-body">
      <h4 class="card-title">Connection Status</h4>
      <p class="text-danger" v-if="!connected">Not connected!</p>
      <p class="text-success" v-if="connected">Connected!</p>
      <div class="form-group">
        <label for="rosbridge-address" class="form-label">ROSBridge Address</label>
        <input
          id="rosbridge-address"
          type="text"
          v-model="rosbridge_address"
          class="form-control"
          placeholder="ws://localhost:9090"
        />
      </div>
      <div class="form-group">
        <label for="webpage-address" class="form-label">WebPage Address</label>
        <input
          id="webpage-address"
          type="text"
          v-model="webpage_adress"
          class="form-control"
          placeholder=""
        />
      </div>
      <div class="mt-3">
        <button
          :disabled="loading"
          class="btn btn-danger me-2"
          @click="disconnect"
          v-if="connected"
        >
          Disconnect
        </button>
        <button :disabled="loading" class="btn btn-success" @click="connect" v-else>
          Connect
        </button>
      </div>
    </div>
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
      webpage_adress:" ",
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
        this.$emit("my-event", this.ros,this.webpage_adress);
      });
      this.ros.on("error", (error) => {
        this.logs.unshift(`${new Date().toTimeString()} - Error: ${error}`);
        this.loading = false;
        console.log("Error conection");
        this.$emit("my-event-error-conection", this.ros);
      });
      this.ros.on("close", () => {
        this.logs.unshift(`${new Date().toTimeString()} - ¡Desconectado!`);
        this.connected = false;
        this.loading = false;
        console.log("Desconectado");
        this.$emit("my-event-disconnect", this.ros);
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
.card {
  max-width: 500px;
  margin: auto;
  border-radius: 15px;
  border: 1px solid #dee2e6;
  background-color: #ffffff;
}

.card-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  font-weight: bold;
  color: #555;
}

.form-control {
  border-radius: 10px;
  border: 1px solid #ced4da;
  padding: 0.5rem 0.75rem;
}

.btn {
  min-width: 100px;
  border-radius: 10px;
}

.text-danger,
.text-success {
  font-weight: bold;
  font-size: 1.1rem;
}

.me-2 {
  margin-right: 0.5rem;
}
</style>