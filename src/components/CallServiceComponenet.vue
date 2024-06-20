<template>
  <div>
    <button @click="handleButtonClick">{{ buttonLabel }}</button>
    <div v-if="response">
      <h3>Output:</h3>
      <pre>{{ response.output }}</pre>
      <h3>Error:</h3>
      <pre>{{ response.error }}</pre>
      <p v-if="response.message">{{ response.message }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "CallServiceComponent",
  data() {
    return {
      response: null,
      buttonLabel: "Init launch file",
      isLaunched: false,
    };
  },
  methods: {
    async handleButtonClick() {
      if (this.isLaunched) {
        await this.stopProcesses();
      } else {
        await this.callLaunchFile();
      }
    },
    async callLaunchFile() {
      try {
        const res = await axios.post('wss://i-07fcfbc3e1d17e5b3.robotigniteacademy.com/05c14792-49c2-4821-99e1-44a490baf3e9/rosbridge/:5000/launch');
        this.response = res.data;
        if (!this.response.error) {
          this.isLaunched = true;
          this.buttonLabel = "Reiniciar servidores";
        }
      } catch (error) {
        console.error('Error launching file:', error);
        this.response = { error: error.message };
      }
    },
    async stopProcesses() {
      try {
        const res = await axios.post('wss://i-07fcfbc3e1d17e5b3.robotigniteacademy.com/05c14792-49c2-4821-99e1-44a490baf3e9/rosbridge/:5000/stop');
        this.response = res.data;
        if (!this.response.error) {
          this.isLaunched = false;
          this.buttonLabel = "Init launch file";
        }
      } catch (error) {
        console.error('Error stopping processes:', error);
        this.response = { error: error.message };
      }
    },
  },
};
</script>

<style>
/* Estilos opcionales */
pre {
  background-color: #f8f8f8;
  padding: 10px;
  border-radius: 5px;
}
</style>
