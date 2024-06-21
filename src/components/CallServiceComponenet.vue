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
    <div class="output-container">
      <h3>Proceso Output:</h3>
      <pre>{{ processOutput.join('\n') }}</pre>
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
      buttonLabel: "Iniciar archivo de lanzamiento",
      isLaunched: false,
      processOutput: [],
      intervalId: null,
    };
  },
  methods: {
    async handleButtonClick() {
      console.log("Button clicked");
      if (this.isLaunched) {
        await this.stopProcesses();
      } else {
        await this.callLaunchFile();
      }
    },
    async callLaunchFile() {
      try {
        console.log("Sending request to launch file");
        const res = await axios.post('https://i-01e38316aa8103772.robotigniteacademy.com/0a429db1-291d-4d1f-95d3-3b3aec993c47/webpage/launch');
        this.response = res.data;
        console.log("Launch response:", this.response);
        if (!this.response.error) {
          this.isLaunched = true;
          this.buttonLabel = "Detener procesos";
          this.startFetchingOutput();
        }
      } catch (error) {
        console.error('Error iniciando archivo de lanzamiento:', error);
        this.response = { error: error.message };
      }
    },
    async stopProcesses() {
      try {
        console.log("Sending request to stop processes");
        const res = await axios.post('https://i-01e38316aa8103772.robotigniteacademy.com/0a429db1-291d-4d1f-95d3-3b3aec993c47/webpage/stop');
        this.response = res.data;
        console.log("Stop response:", this.response);
        if (!this.response.error) {
          this.isLaunched = false;
          this.buttonLabel = "Iniciar archivo de lanzamiento";
          this.stopFetchingOutput();
        }
      } catch (error) {
        console.error('Error deteniendo procesos:', error);
        this.response = { error: error.message };
      }
    },
    startFetchingOutput() {
      this.intervalId = setInterval(this.fetchOutput, 1000);
    },
    stopFetchingOutput() {
      if (this.intervalId) {
        clearInterval(this.intervalId);
        this.intervalId = null;
      }
    },
    async fetchOutput() {
      try {
        const res = await axios.get('https://i-01e38316aa8103772.robotigniteacademy.com/0a429db1-291d-4d1f-95d3-3b3aec993c47/webpage/output');
        this.processOutput = res.data;
      } catch (error) {
        console.error('Error fetching process output:', error);
      }
    },
  },
  beforeDestroy() {
    this.stopFetchingOutput();
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

.output-container {
  height: 300px; /* Puedes ajustar la altura según tus necesidades */
  overflow-y: scroll;
  background-color: #f8f8f8;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
}
</style>
