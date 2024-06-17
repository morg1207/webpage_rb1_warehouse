<template>
  <div class="col-6">
    <div class="card-header">
      <h4>Joystick</h4>
    </div>
    <div class="card-body">
      <div id="dragstartzone" @mousedown="startDrag" @mousemove="doDrag"></div>
      <div id="dragCircle" :style="dragCircleStyle"></div>
    </div>
  </div>
  <div class="col-6">
    <div class="card-header">
      <h4>Joystick values</h4>
    </div>
    <div class="card-body">
      <hr />
      <p>Vertical: {{ joystick.vertical.toFixed(3) }}</p>
      <br />
      <p>Horizontal: {{ joystick.horizontal.toFixed(3) }}</p>
    </div>
  </div>
</template>

<script>
import ROSLIB from "roslib";

export default {
  name: "JoystickComponent",
  data() {
    return {
      // values
      ros: null,
      // publisher
      pubInterval: null,
      joystick: {
        vertical: 0,
        horizontal: 0,
      },
      // joystick grapth
      dragging: false,
      x: "no",
      y: "no",
      dragCircleStyle: {
        margin: "0px",
        top: "0px",
        left: "0px",
        display: "none",
        width: "75px",
        height: "75px",
      },
      topic_cmd_vel: "cmd_vel",
    };
  },

  methods: {
    joystickConfig(ros) {
      console.log("Joystick configurado");
      this.ros = ros;
      this.pubInterval = setInterval(this.publishCmdVel, 100);
    },
    paramConfig(config_web) {
      console.log(config_web);
      this.topic_name = config_web.topic_cmd_vel.value;
    },
    //enviar velocidades
    publishCmdVel: function () {
      let topic = new ROSLIB.Topic({
        ros: this.ros,
        name: "cmd_vel",
        messageType: "geometry_msgs/msg/Twist",
      });
      let message = new ROSLIB.Message({
        linear: { x: this.joystick.vertical, y: 0, z: 0 },
        angular: { x: 0, y: 0, z: -1 * this.joystick.horizontal },
      });
      console.log("Publicando mensaje");
      topic.publish(message);
      
    },

    // funciones para el joystick
    startDrag() {
      this.dragging = true;
      this.x = this.y = 0;
    },
    stopDrag() {
      this.dragging = false;
      this.x = this.y = "no";
      this.dragCircleStyle.display = "none";
      this.resetJoystickVals();
    },
    doDrag(event) {
      if (this.dragging) {
        this.x = event.offsetX;
        this.y = event.offsetY;
        let ref = document.getElementById("dragstartzone");
        this.dragCircleStyle.display = "inline-block";

        let minTop = ref.offsetTop - parseInt(this.dragCircleStyle.height) / 2;
        //let maxTop = minTop + 200;
        let top = this.y + minTop;
        this.dragCircleStyle.top = `${top}px`;

        let minLeft = ref.offsetLeft - parseInt(this.dragCircleStyle.width) / 2;
        //let maxLeft = minLeft + 200;
        let left = this.x + minLeft;
        this.dragCircleStyle.left = `${left}px`;
        this.setJoystickVals();
      }
    },
    setJoystickVals() {
      this.joystick.vertical = -1 * (this.y / 200 - 0.5);
      this.joystick.horizontal = +1 * (this.x / 200 - 0.5);
    },
    resetJoystickVals() {
      this.joystick.vertical = 0;
      this.joystick.horizontal = 0;
    },
  },
  mounted() {
    // page is ready
    window.addEventListener("mouseup", this.stopDrag);
    this.interval = setInterval(() => {
      if (this.ros != null && this.ros.isConnected) {
        this.ros.getNodes(
          (data) => {
            console.log(data);
          },
          (error) => {
            console.log(error);
          }
        );
      }
    }, 10000);
  },
};
</script>

<style scoped>
/* Add any styles specific to the map component here */
</style>
