<template>
  <div class="card-header">
    <h4>Logs</h4>
  </div>
  <div class="card-body logs-container">
    <p v-for="(log, index) in logs" :key="index">{{ log }}</p>
  </div>
</template>

<script>
export default {
  name: "LogsComponent",
  data() {
    return {
      ros: null,
      logs: [],
    };
  },
  methods: {
    logsInit() {
      this.logs.unshift(new Date().toTimeString() + " - Connected!");
    },
  },
};
</script>

<style scoped>
.logs-container {
  max-height: 90px; /* Ajusta esta altura según tus necesidades */
  overflow-y: auto; /* Habilita el desplazamiento vertical */
}
</style>