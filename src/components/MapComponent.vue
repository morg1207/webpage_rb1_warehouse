<template>
  <div class="card-header">
    <h4>Map</h4>
  </div>
  <div class="card-body">
    <canvas id="mapCanvas"></canvas>
  </div>
</template>

<script>
import ROSLIB from "roslib";

export default {
  name: "MapComponent",
  data() {
    return {
      //map
      ros: null,
      mapViewer: null,
      mapGridClient: null,
      interval: null,
      state: false,

      // publisher
      pubInterval: null,

      map: null,
      context: null,
      scale: 5,
      point_last_x: 0,
      point_last_y: 0,
    };
  },

  methods: {
    // map subscribe
    setMapViewer(ros) {
      console.log("Set map viewer");
      this.connected = true;
      let topic = new ROSLIB.Topic({
        ros: ros,
        name: "/map",
        messageType: "nav_msgs/msg/OccupancyGrid",
      });
      topic.subscribe((map) => {
        this.drawAll(map);
        console.log("Map subscriber");
      });
    },
    // amcl_pose subscribe
    amclPose(ros) {
      console.log("Config subscriber amcl_pose");
      this.connected = true;
      let topic = new ROSLIB.Topic({
        ros: ros,
        name: "/amcl_pose",
        messageType: "geometry_msgs/msg/PoseWithCovarianceStamped",
      });
      topic.subscribe((message) => {
        console.log("Amcl pose ");
        this.drawRobot(
          this.map,
          this.context,
          message.pose.pose.position.x,
          message.pose.pose.position.y
        );
        console.log(message);
      });
    },

    drawAll(map) {
      this.map = map;
      const width = map.info.width;
      const height = map.info.height;
      const origin_x = map.info.origin.position.x;
      const origin_y = map.info.origin.position.y;
      const resolution = map.info.resolution;
      console.log("Map scale");
      console.log(this.$parentscale);
      console.log("Map height");
      console.log(height);
      console.log("Map width");
      console.log(width);
      console.log("Map resolution");
      console.log(resolution);
      console.log("Map origin x");
      console.log(origin_x);
      console.log("Map origin y");
      console.log(origin_y);

      // Get the canvas and context
      const canvas = document.getElementById("mapCanvas");
      const context = canvas.getContext("2d");
      this.context = context;

      this.drawMap(map, canvas, context);
      this.drawGrid(map, context);
    },
    drawMap(map, canvas, context) {
      var data = map.data;

      const width = map.info.width;
      const height = map.info.height;

      // Initialize data_1 to store reflected data
      const data_1 = new Array(data.length);

      // Set canvas dimensions to the original map dimensions
      canvas.width = width * this.scale;
      canvas.height = height * this.scale;

      // Create a new ImageData object
      const imageData = context.createImageData(
        width * this.scale,
        height * this.scale
      );

      // Populate the image data with values
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          const index = y * width + x;
          data_1[index] = data[(y + 1) * width - x - 1];
          const value = data_1[index];
          const color = value === -1 ? 255 : 255 - (value / 100) * 255;

          /*const scaledIndex = (y * width + x) * 4;
          imageData.data[scaledIndex] = color; // Red
          imageData.data[scaledIndex + 1] = color; // Green
          imageData.data[scaledIndex + 2] = color; // Blue
          imageData.data[scaledIndex + 3] = 255; // Alpha*/
          for (let dy = 0; dy < this.scale; dy++) {
            for (let dx = 0; dx < this.scale; dx++) {
              const scaledIndex =
                ((y * this.scale + dy) * width * this.scale +
                  (x * this.scale + dx)) *
                4;
              imageData.data[scaledIndex] = color; // Red
              imageData.data[scaledIndex + 1] = color; // Green
              imageData.data[scaledIndex + 2] = color; // Blue
              imageData.data[scaledIndex + 3] = 255; // Alpha
            }
          }
        }
      }

      // Draw the image data onto the canvas
      context.putImageData(imageData, 0, 0);

      // Draw the grid
    },

    drawGrid(map, context) {
      this.map = map;

      const width = map.info.width;
      const height = map.info.height;
      context.strokeStyle = "rgba(0, 0, 0, 0.8)"; // Light grey grid lines
      context.lineWidth = 0.5;

      // Draw vertical lines
      for (let x = 0; x <= width * this.scale; x += 100) {
        context.beginPath();
        context.moveTo(x, 0);
        context.lineTo(x, height * this.scale);
        context.stroke();
      }

      // Draw horizontal lines
      for (let y = 0; y <= height * this.scale; y += 100) {
        context.beginPath();
        context.moveTo(0, y);
        context.lineTo(width * this.scale, y);
        context.stroke();
      }
    },
    drawRobot(map, context, point_x, point_y) {
      const radius = 5; // Radio del punto
      context.clearRect(
        this.point_last_x - (radius + 5) / 2,
        this.point_last_y - (radius + 5) / 2,
        radius + 5,
        radius + 5
      );
      const origin_x = map.info.origin.position.x;
      const origin_y = map.info.origin.position.y;
      const resolution = map.info.resolution;
      console.log("Coordenadas origin");
      console.log(origin_x);
      console.log(origin_y);

      // Dibujar el punto en el canvas
      const point_x_index =
        this.map.info.width * this.scale -
        ((point_x - origin_x) * this.scale) / resolution;
      const point_y_index = -((origin_y - point_y) * this.scale) / resolution;

      context.beginPath();
      context.arc(point_x_index, point_y_index, radius, 0, 2 * Math.PI);

      context.fillStyle = "red"; // Color del punto
      context.fill();
      context.closePath();
      this.point_last_x = point_x_index;
      this.point_last_y = point_y_index;
    },
  },
};
</script>

<style scoped>
/* Estilos para el contenedor del mapa */
#mapContainer {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Estilos para el canvas del mapa */
#mapCanvas {
  max-width: 100%;
  max-height: 100%;
}
</style>
