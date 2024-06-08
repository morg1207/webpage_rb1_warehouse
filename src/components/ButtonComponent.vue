<template>
  <button
    :class="buttonClass"
    @click="handleClick"
    :disabled="state === 'processing'"
  >
    <span v-if="state === 'processing'" class="spinner"></span>
    <span v-else>{{ buttonText }}</span>
  </button>
</template>

<script>
export default {
  name: "StatefulButton",
  props: {
    initialState: {
      type: String,
      default: "inactive", // Can be 'inactive', 'active', or 'processing'
    },
  },
  data() {
    return {
      state: this.initialState,
    };
  },
  computed: {
    buttonText() {
      switch (this.state) {
        case "active":
          return "Activated";
        case "inactive":
          return "Deactivated";
        case "processing":
          return "Processing...";
        default:
          return "Unknown State";
      }
    },
    buttonClass() {
      return {
        button: true,
        active: this.state === "active",
        inactive: this.state === "inactive",
        processing: this.state === "processing",
      };
    },
  },
  methods: {
    handleClick() {
      if (this.state === "inactive") {
        this.state = "processing";
        setTimeout(() => {
          this.state = "active";
        }, 2000); // Simulate an asynchronous operation
      } else if (this.state === "active") {
        this.state = "processing";
        setTimeout(() => {
          this.state = "inactive";
        }, 2000); // Simulate an asynchronous operation
      }
    },
  },
};
</script>

<style scoped>
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

.button:disabled {
  opacity: 0.6;
}

.spinner {
  border: 4px solid rgb
}
</style>
