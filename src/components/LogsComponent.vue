<template>
  <div class="card-header">
    <h4>Logs</h4>
  </div>
  <div class="card-body">
    <p v-for="(log, index) in logs" :key="index">{{ log }}</p>
  </div>
</template>

<script>
export default {
  name: "MapComponent",
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
