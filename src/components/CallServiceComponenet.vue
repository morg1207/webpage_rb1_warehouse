<template>
  <div>
    <button :class="buttonClass" @click="handleButtonClick" :disabled="isDisabled">{{ buttonLabel }}</button>
    <div v-if="response">
      <h5>Output:</h5>
      <pre>{{ response.output }}</pre>
      <h5>Error:</h5>
      <pre>{{ response.error }}</pre>
      <p v-if="response.message">{{ response.message }}</p>
    </div>
    <div class="output-container">
      <h5>Process Output:</h5>
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
      isDisabled: true, // Botón inicialmente deshabilitado
      state: 'inactive',
      webpage_adress: '',
    };
  },
  computed: {
    buttonClass() {
      return {
        'button': true,
        'active': this.state === "active",
        'inactive': this.state === "inactive",
        'processing': this.state === "processing",
        'disabled': this.isDisabled,
      };
    },
  },
  methods: {
    callServiceInit(webpage_adress){
      this.webpage_adress = webpage_adress,
      console.log('webpage_adress' + webpage_adress);
      console.log('Call service enable');
      this.enableButton();
    },

    callServiceClose(){
      console.log('Call service dissable');
      this.disableButton();

    },
    disableButton() {
      this.isDisabled = true;
    },
    enableButton() {
      this.isDisabled = false;
    },
    async handleButtonClick() {
      console.log("Button clicked");
      this.isDisabled = true;
      this.state = "processing";
      if (this.isLaunched) {
        await this.stopProcesses();
        this.$emit("my-event-stop-service");
        console.log("Evento de stop service emitido");
      } else {
        await this.callLaunchFile();
        console.log("Evento de call service emitido");
      }
    },
    async callLaunchFile() {
      try {
        console.log("Sending request to launch file");
        const res = await axios.post(this.webpage_adress + 'launch');
        console.log(this.webpage_adress + 'launch');
        this.response = res.data;
        console.log("Launch response:", this.response);
        if (!this.response.error) {
          this.isLaunched = true;
          this.buttonLabel = "Reiniciar servidores";
          this.state = "active";
          this.$emit("my-event-call-service");
          this.startFetchingOutput();
        } else {
          this.state = "inactive";
        }
      } catch (error) {
        console.error('Error iniciando archivo de lanzamiento:', error);
        this.response = { error: error.message };
        this.state = "inactive";
      } finally {
        this.isDisabled = false;
      }
    },
    async stopProcesses() {
      try {
        console.log("Sending request to stop processes");
        const res = await axios.post(this.webpage_adress+ 'stop');
        this.response = res.data;
        console.log("Stop response:", this.response);
        if (!this.response.error) {
          this.isLaunched = false;
          this.buttonLabel = "Iniciar archivo de lanzamiento";
          this.state = "inactive";
          this.stopFetchingOutput();
        }
      } catch (error) {
        console.error('Error deteniendo procesos:', error);
        this.response = { error: error.message };
      } finally {
        this.isDisabled = false;
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
        const res = await axios.get(this.webpage_adress+'output');
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

<style scoped>
/* Estilos opcionales */
pre {
  background-color: #f8f8f8;
  padding: 10px;
  border-radius: 5px;
}

.output-container {
  height: 500px; /* Puedes ajustar la altura según tus necesidades */
  overflow-y: scroll;
  background-color: #f8f8f8;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.inactive {
  background-color: #f44336;
  color: white;
}

.active {
  background-color: #4caf50;
  color: white;
}

.processing {
  background-color: #ffc107;
  color: white;
  cursor: not-allowed;
}

.disabled {
  background-color: #ccc;
  color: #666;
  cursor: not-allowed;
  opacity: 0.6;
}
</style>
