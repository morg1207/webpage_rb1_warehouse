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
import robotImageSrc from "@/assets/robot.png"; // Import the image
import shelfImageSrc from "@/assets/shelf.png"; // Import the image
import robotWithShelfImageSrc from "@/assets/robot_shelf.png"; // Import the image


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

      points: [
        { x: -0.19, y: 1.3, z: 0.708, w: 0.706, label: "A" },
        { x: -1.987, y: 0.109, z: 1.0, w: 0, label: "B" },
        { x: -1.9906, y: -1.447, z: 1.0, w: 0, label: "C" },
        { x: 1.986, y: -1.228, z: -0.695, w: 0.719, label: "D" },
        // Añade más puntos según sea necesario
      ], 
      mapCanvas: null,
      mapContext: null,
      mainCanvas: null,
      mainContext: null,

      scale: 5,
      point_last_x_robot: 0,
      point_last_y_robot: 0,
      point_last_x_shelf: 0,
      point_last_y_shelf: 0,
      point_last_angle_shelf: 0,
      robotImage: new Image(), // Initialize the robot image
      shelfImage: new Image(), // Initialize the robot image
      robotWithShelfImage: new Image(), // Initialize the robot image
      shelf_detected: false,
      robot_state_figure: 'only_robot'
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
      this.robotImage.src = robotImageSrc;
      this.shelfImage.src = shelfImageSrc;
      this.robotWithShelfImage.src = robotWithShelfImageSrc;
    },
    mapClose(){
      console.log("Close Map");
      if(this.mapContext != null && this.mainContext !=null) {

        this.mapContext.clearRect(0, 0, this.mapCanvas.width, this.mapCanvas.height);
        this.mainContext.clearRect(0, 0, this.mainCanvas.width, this.mainCanvas.height);
      }


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
        const position = message.pose.pose.position;
        const orientation = message.pose.pose.orientation;
        const angle = this.quaternionToAngle(orientation);
        this.drawRobot(position.x, position.y, angle, this.robot_state_figure);
        console.log(message);
      });
    },

    // Shelf Subscription
    shelfPose(ros) {
      console.log("subscritpion pose shelf");
      this.connected = true;
      let topic = new ROSLIB.Topic({
        ros: ros,
        name: "/shelf_pose",
        messageType: "geometry_msgs/msg/Pose",
      });
      topic.subscribe((message) => {
        console.log("Shelf pose ");
        const position = message.position;
        const orientation = message.orientation;
        const angle = this.quaternionToAngle(orientation);
        this.drawShelf(position.x, position.y, angle);
        console.log(message);
        this.shelf_detected = true;
      });
    },

    // Robot subscription
    RobotStateFIgure(ros) {
      console.log("subscritpion robot state figure");
      this.connected = true;
      let topic = new ROSLIB.Topic({
        ros: ros,
        name: "/robot_state_figure",
        messageType: "std_msgs/msg/String",
      });
      topic.subscribe((message) => {
        console.log(`Robot state figure recibido  ${message.data}`)
        this.robot_state_figure = message.data
      });
    },

    quaternionToAngle(q) {
      const siny_cosp = 2 * (q.w * q.z + q.x * q.y);
      const cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z);
      return Math.atan2(siny_cosp, cosy_cosp);
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

      this.mapCanvas = document.createElement("canvas");
      this.mapContext = this.mapCanvas.getContext("2d");

      this.mainCanvas = document.getElementById("mapCanvas");
      this.mainContext = this.mainCanvas.getContext("2d");

      // Set offscreen canvas size
      this.mapCanvas.width = width * this.scale;
      this.mapCanvas.height = height * this.scale;

      this.drawMap(map, this.mapContext);
      this.drawGrid(map, this.mapContext);

      // Set main canvas size
      this.mainCanvas.width = width * this.scale;
      this.mainCanvas.height = height * this.scale;

      // Draw the static map and grid on the main canvas
      this.mainContext.drawImage(this.mapCanvas, 0, 0);

    },
    drawMap(map, context) {
      var data = map.data;

      const width = map.info.width;
      const height = map.info.height;

      // Initialize data_1 to store reflected data
      const data_1 = new Array(data.length);

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
      // Draw yellow boxes based on points array

      const origin_x = this.map.info.origin.position.x;
      const origin_y = this.map.info.origin.position.y;
      const resolution = this.map.info.resolution;


      context.strokeStyle = 'yellow';
      context.lineWidth = 7;
      context.font = `${25}px Arial`; // Ajusta el tamaño de la fuente
      context.fillStyle = 'black'; // Color del texto
      this.points.forEach(point => {

        const point_x_index =
        this.map.info.width * this.scale -
        ((point.x - origin_x) * this.scale) / resolution;
        const point_y_index = -((origin_y - point.y) * this.scale) / resolution;

        const boxSize = 14 * this.scale; // Define el tamaño del cuadro amarillo
        const scaledX = point_x_index - boxSize/2 ;
        const scaledY = point_y_index- boxSize/2;
        

        context.strokeRect(scaledX, scaledY, boxSize, boxSize);
        //Texto
        // Escribe el texto en el centro del cuadro
        const textX = scaledX + boxSize / 2;
        const textY = scaledY + boxSize / 2;
        context.textAlign = 'center';
        context.textBaseline = 'middle';
        context.fillText(point.label, textX, textY);
      });
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
    drawRobot(point_x, point_y, angle, robot_state_figure) {
      const radius = 5;
      this.mainContext.clearRect(
        this.point_last_x_robot - (radius + 5) / 2,
        this.point_last_y_robot - (radius + 5) / 2,
        radius + 5,
        radius + 5
      );
      const origin_x = this.map.info.origin.position.x;
      const origin_y = this.map.info.origin.position.y;
      const resolution = this.map.info.resolution;

      const point_x_index =
        this.map.info.width * this.scale -
        ((point_x - origin_x) * this.scale) / resolution;
      const point_y_index = -((origin_y - point_y) * this.scale) / resolution;
      // Define the size of the image
      const imageSize = 100; // Change this value to scale the image
      // Draw the robot image with rotation


      // Calculate the clear area size based on the image size
      const clearSize = imageSize + 10;

      // Clear the previous robot image area
      this.mainContext.clearRect(
        this.point_last_x_robot - clearSize / 2,
        this.point_last_y_robot - clearSize / 2,
        clearSize,
        clearSize
      );
      // Redraw the static map and grid
      this.mainContext.drawImage(this.mapCanvas, 0, 0);

      if(robot_state_figure == 'only_robot'){
        if (this.robotImage.complete) {
          this.mainContext.save();
          this.mainContext.translate(point_x_index, point_y_index);
          this.mainContext.rotate(-angle- Math.PI/2);
          this.mainContext.drawImage(this.robotImage, -imageSize / 2, -imageSize / 2, imageSize, imageSize);
          this.mainContext.restore();
          console.log("Dibujando robot");
        } else {
          this.robotImage.onload = () => {
            this.mainContext.save();
            this.mainContext.translate(point_x_index, point_y_index);
            this.mainContext.rotate(-angle- Math.PI/2);
            this.mainContext.drawImage(this.robotImage, -imageSize / 2, -imageSize / 2, imageSize, imageSize);
            this.mainContext.restore();
          };
        }
        if(this.shelf_detected){
            console.log("Dibujando shelf");
            this.drawShelf(this.point_last_x_shelf, this.point_last_y_shelf, this.point_last_angle_shelf);
        };
      }
      if(robot_state_figure == 'robot_with_shelf'){
        if (this.robotWithShelfImage.complete) {
          this.mainContext.save();
          this.mainContext.translate(point_x_index, point_y_index);
          this.mainContext.rotate(-angle- Math.PI/2);
          this.mainContext.drawImage(this.robotWithShelfImage, -imageSize / 2, -imageSize / 2, imageSize, imageSize);
          this.mainContext.restore();
          console.log("Dibujando robot with shelf");
        } else {
          this.robotWithShelfImage.onload = () => {
            this.mainContext.save();
            this.mainContext.translate(point_x_index, point_y_index);
            this.mainContext.rotate(-angle- Math.PI/2);
            this.mainContext.drawImage(this.robotWithShelfImage, -imageSize / 2, -imageSize / 2, imageSize, imageSize);
            this.mainContext.restore();
          };
        }
      }

      this.point_last_x_robot = point_x_index;
      this.point_last_y_robot = point_y_index;
    },

    drawShelf(point_x, point_y, angle) {
      const radius = 5;
      this.mainContext.clearRect(
        this.point_last_x_shelf - (radius + 5) / 2,
        this.point_last_y_shelf - (radius + 5) / 2,
        radius + 5,
        radius + 5
      );
      const origin_x = this.map.info.origin.position.x;
      const origin_y = this.map.info.origin.position.y;
      const resolution = this.map.info.resolution;

      const point_x_index =
        this.map.info.width * this.scale -
        ((point_x - origin_x) * this.scale) / resolution;
      const point_y_index = -((origin_y - point_y) * this.scale) / resolution;
      // Define the size of the image
      const imageSize = 100; // Change this value to scale the image
      // Draw the robot image with rotation


      // Calculate the clear area size based on the image size
      const clearSize = imageSize + 10;

      // Clear the previous robot image area
      this.mainContext.clearRect(
        this.point_last_x_shelf - clearSize / 2,
        this.point_last_y_shelf - clearSize / 2,
        clearSize,
        clearSize
      );
      // Redraw the static map and grid
      if (this.shelfImage.complete) {
        this.mainContext.save();
        this.mainContext.translate(point_x_index, point_y_index);
        this.mainContext.rotate(-angle + Math.PI/2);
        this.mainContext.drawImage(this.shelfImage, -imageSize / 2, -imageSize / 2, imageSize, imageSize);
        this.mainContext.restore();
      } else {
        this.shelfImage.onload = () => {
          this.mainContext.save();
          this.mainContext.translate(point_x_index, point_y_index);
          this.mainContext.rotate(-angle+ Math.PI/2);
          this.mainContext.drawImage(this.sehlfImage, -imageSize / 2, -imageSize / 2, imageSize, imageSize);
          this.mainContext.restore();
        };
      }

      this.point_last_x_shelf = point_x;
      this.point_last_y_shelf = point_y;
      this.point_last_angle_shelf = angle;
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
