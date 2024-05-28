<template>
  <div class="app-container">
    <h5>Load ROS Parameters</h5>
    <input type="file" @change="onFileChange" />
    <button @click="loadParameters" :disabled="!fileContent">
      Load Parameters
    </button>
  </div>
</template>

<script>
import ROSLIB from "roslib";
export default {
  name: "ParamsComponent",

  data() {
    return {
      ros: null,
      fileContent: null,
      nodeName: "/turtlesim",
      parameters: null,
      config_web: null,
    };
  },
  methods: {
    paramInit(ros) {
      console.log("Parametros config");
      this.ros = ros;
    },
    loadParameters() {
      if (this.fileContent) {
        try {
          console.log("Parametros cargando");
          this.parameters = JSON.parse(this.fileContent);
          console.log(this.parameters);
        } catch (error) {
          console.error("Invalid JSON file:", error);
        }
      }
      console.log("Procesando");
      // Extraer los nombres de los nodos de mayor nivel
      const topLevelNodes = Object.keys(this.parameters);
      console.log(topLevelNodes);
      for (let nodeName of topLevelNodes) {
        console.log(`Nodo: ${nodeName}`);
        const nodeContent = this.parameters[nodeName];
        console.log("Contenido:");
        console.log(nodeContent);

        if (nodeName === "web") {
          // Si el nodeName es "web", guarda su contenido en config_web
          console.log("[Params Component] emit event");
          this.config_web = nodeContent;
          this.$emit("event_config_web", this.config_web);
        } else {
          // Si no, llama a la función createClient
          this.createClient(nodeName, nodeContent);
          // emito un evento
        }
      }
    },
    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.fileContent = e.target.result;
        };
        reader.readAsText(file);
      }
    },
    createClient(nodeName, parameters) {
      // Crear un cliente de servicio para cargar parámetros
      const paramClient = new ROSLIB.Service({
        ros: this.ros,
        name: nodeName + "/set_parameters", // Nombre del servicio para cargar parámetros
        serviceType: "rcl_interfaces/srv/SetParameters", // Tipo de servicio para cargar parámetros
      });
      console.log(`Create client  a : ${nodeName}`);
      console.log(parameters["parameters"]);
      // Crear una solicitud para cargar los parámetros
      const request = new ROSLIB.ServiceRequest({
        //parameters,
        parameters: parameters["parameters"],
      });

      // Enviar la solicitud al nodo para cargar los parámetros
      console.log("Call to service parameter");
      paramClient.callService(
        request,
        function (response) {
          console.log("Parámetros cargados exitosamente:", response);
        },
        function (error) {
          console.log("Error al cargar los parámetros:", error);
        }
      );
    },
  },
};
</script>

<style scoped>
/* Add any styles specific to the config page here */
</style>
