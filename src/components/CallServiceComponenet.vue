<template>
  <div>
    <button @click="callLaunchFile">Launch ROS2 File</button>
    <div v-if="response">
      <h3>Output:</h3>
      <pre>{{ response.output }}</pre>
      <h3>Error:</h3>
      <pre>{{ response.error }}</pre>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      response: null,
    };
  },
  methods: {
    async callLaunchFile() {
      try {
        const res = await axios.post('http://localhost:5000/launch');
        this.response = res.data;
      } catch (error) {
        console.error('Error launching file:', error);
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