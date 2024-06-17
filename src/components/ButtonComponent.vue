<template>
  <div>
    <button
      :class="buttonClass"
      @click="handleClick"
      :disabled="state !== 'active'"
    >
      <span v-if="state === 'processing'" class="spinner"></span>
      <span v-else>{{ buttonText }}</span>
    </button>
    <p v-if="state === 'processing'" class="processing-text"> {{buttonTextProcessing}}</p>
  </div>
</template>

<script>
import ROSLIB from 'roslib';

export default {
  name: "StatefulButton",
  props: {
    initialState: {
      type: String,
      default: "inactive", // Can be 'inactive', 'active', or 'processing'
    },
    buttonTextActive: {
      type: String,
      default: "InitLocalization", // Text when button is active
    },

    buttonTextInactive: {
      type: String,
      default: "Deactivated", // Text when button is inactive
    },
    buttonTextProcessing: {
      type: String,
      default: "Localizando...", // Text when button is in processing state
    },
    buttonPublishBT: {
      type: String,
      default: "find_shelf_and_publish", // Text when button is in processing state
    },
  },
  data() {
    return {
      state: this.initialState,
      ros: null,
    };
  },
  computed: {
    buttonText() {
      switch (this.state) {
        case "active":
          return this.buttonTextActive;
        case "inactive":
          return this.buttonTextInactive;
        case "processing":
          return this.buttonTextProcessing;
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
    buttonInit(ros) {
      console.log("Set button config");
      this.activateButton();
      this.publishTopic = new ROSLIB.Topic({
        ros: ros,
        name: "/bt_selector",
        messageType: "std_msgs/msg/String",
      });
      let subscribeBtStatus = new ROSLIB.Topic({
        ros: ros,
        name: "/bt_status",
        messageType: "std_msgs/msg/String",
      });
      subscribeBtStatus.subscribe((message) => {
        if (message.data === this.buttonPublishBT + '/done') {
          this.state = "active";
        }
      });
    },


    handleClick() {
      if (this.state === "active") {
        this.state = "processing";
        this.publishTopic.publish(new ROSLIB.Message({ data: this.buttonPublishBT }));
      }
    },
    activateButton() {
      this.state = "active";
    },
    deactivateButton() {
      this.state = "inactive";
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
  opacity: 0.6;
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
  cursor: not-allowed;
}

.spinner {
  border: 4px solid rgba(255, 255, 255, 0.6);
  border-top: 4px solid white;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
}

.processing-text {
  margin-top: 10px;
  font-size: 14px;
  color: #ffc107;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
