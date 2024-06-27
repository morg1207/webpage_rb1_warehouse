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
    <!-- Agregar los botones cuadrados debajo del botón principal -->

    <div v-if="showSubButtons">
      <button class="sub-button" @click="handleSubButtonClick('A')">A</button>
      <button class="sub-button" @click="handleSubButtonClick('B')">B</button>
      <button class="sub-button" @click="handleSubButtonClick('C')">C</button>
      <button class="sub-button" @click="handleSubButtonClick('D')">D</button>
    </div>
    <!-- Label que se modifica al hacer clic en el botón -->
    <div v-if="showSubButtons">
      <p>{{ labelText }}</p>
    </div>
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
    buttonPublishFigure: {
      type: String,
      default: "only_robot", // Text when button is in processing state
    },
  },
  data() {
    return {
      state: this.initialState,
      ros: null,
      showSubButtons: false, // Agregar estado para mostrar los botones cuadrados
      points: [
        { x: -0.19, y: 1.3, z: 0.708, w: 0.706, label: "A" },
        { x: -1.987, y: 0.109, z: 1.0, w: 0, label: "B" },
        { x: -1.9906, y: -1.447, z: 1.0, w: 0, label: "C" },
        { x: 1.986, y: -1.228, z: -0.695, w: 0.719, label: "D" },
        // Añade más puntos según sea necesario
      ], 
      labelText: '', // Nuevo estado para el label
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
      this.publishTopicFigureState = new ROSLIB.Topic({
        ros: ros,
        name: "/robot_state_figure",
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
          this.labelText = ""; // Actualiza el texto del label
          this.publishTopicFigureState.publish(new ROSLIB.Message({ data: this.buttonPublishFigure }));
          console.log(`------`)
          console.log(`Publicado figure state  ${this.buttonPublishFigure}`)
          console.log(`------`)
        }
      });
    },
    buttonClose() {
      if (this.subscribeBtStatus) {
        this.subscribeBtStatus.unsubscribe();
        this.subscribeBtStatus = null;
      }
      if (this.publishTopic) {
        this.publishTopic.unadvertise();
        this.publishTopic = null;
      }
      this.showSubButtons = false;
      console.log('Close button')
      this.deactivateButton();
      this.labelText = " "; // Actualiza el texto del label
    },

    buttonShowSubButtons(ros){

      this.publishPoseNavTopic = new ROSLIB.Topic({
        ros: ros,
        name: "/pose_discharge_nav",
        messageType: "geometry_msgs/msg/Pose",
      });

      this.showSubButtons = true;
    },

    handleClick() {
      if (this.state === "active") {
        this.state = "processing";
        this.publishTopic.publish(new ROSLIB.Message({ data: this.buttonPublishBT }));
        this.labelText = "select a navigation position "; // Actualiza el texto del label

      }
    },
    activateButton() {
      this.state = "active";
    },
    deactivateButton() {
      this.state = "inactive";
    },
    handleSubButtonClick(label) {
      // Aquí puedes manejar la lógica para cada botón cuadrado
      let message = new ROSLIB.Message({
            position: { x: 0.0, y: 0.0, z: 0 },
            orientation: { x: 0., y: 0., z: 0.0, w: 1.0 },
        });

      for (let i = 0; i < this.points.length; i++) {
        if (this.points[i].label === label) {
          message = new ROSLIB.Message({
            position: { x: this.points[i].x, y: this.points[i].y, z: 0. },
            orientation: { x: 0., y: 0., z: this.points[i].z, w: this.points[i].w },
          });
        }
      }
      this.publishPoseNavTopic.publish(message);
      console.log(`Botón cuadrado ${number} presionado`);
      console.log(`Enviando punto de naveagcion x : ${this.points[i].x}`);
      console.log(`Enviando punto de naveagcion y : ${this.points[i].y}`);
      console.log(`Enviando punto de naveagcion z : ${this.points[i].z}`);
      console.log(`Enviando punto de naveagcion w : ${this.points[i].w}`);

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
/* Estilos para los botones cuadrados */
.sub-button {
  display: inline-block;
  margin: 5px;
  padding: 10px;
  border: 2px solid #333;
  border-radius: 5px;
  background-color: #eee;
  color: #333;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}
.sub-button:hover {
  background-color: #ccc;
  color: #fff;
}
</style>
