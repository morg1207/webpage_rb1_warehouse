<script setup>

  import MapComponent from "./components/MapComponent.vue";
  import RobotConfigComponent from "./components/RobotConfigComponent.vue";
  import ButtonComponent from "./components/ButtonComponent.vue";
  import JoystickComponent from "./components/JoystickComponent.vue";
  import LogsComponent from "./components/LogsComponent.vue";
  import ParamsComponent from "./components/ParamsComponent.vue";

  import CallServiceComponent from "./components/CallServiceComponenet.vue";


</script>

<template>
  <div id="app" class="container-fluid">
    <div class="row">
      <div class="col-2 text-center">
        <!-- Connect-->
        <div class="card mt-2">
          <RobotConfigComponent @my-event="connect_ros"></RobotConfigComponent>
        </div>

        <!--Log-->
        <div class="card mt-2">
          <LogsComponent
            ref="LogsComponentRef"
            v:bind:usuario="usuario"
          ></LogsComponent>
        </div>
        <!-- Load file-->
        <div class="card mt-2">
          <ParamsComponent
            @event_config_web="config_web_event"
            ref="ParamsComponentRef"
            v:bind:usuario="usuario"
          ></ParamsComponent>
        </div>
      </div>
      <!--Map-->
      <div class="col-6" style="overflow: auto">
        <div class="map-column">
          <MapComponent
            ref="MapComponentRef"
            v:bind:usuario="usuario"
          ></MapComponent>
        </div>
      </div>
      <!--Botones-->
      <div class="col-1 button-container">
        <div class="button-column">
          <ButtonComponent
            ref="ButtonInitLocComponentRef"
            v:bind:usuario="usuario"
            :initialState="'inactive'"
            :buttonTextActive="'Init Localization'"
            :buttonTextInactive="'Deactivated'"
            :buttonTextProcessing="'Localizando robot...'"
            :buttonPublishBT="'init_localization'"
            >
        </ButtonComponent>
        </div>
        <div class="button-column">
          <ButtonComponent
            ref="ButtonFindShelfComponentRef"
            v:bind:usuario="usuario"
            :initialState="'inactive'"
            :buttonTextActive="'Find shelf'"
            :buttonTextInactive="'Deactivated'"
            :buttonTextProcessing="'Finding shelf...'"
            :buttonPublishBT="'find_shelf_and_publish'"
          ></ButtonComponent>
        </div>
        <div class="button-column">
          <ButtonComponent></ButtonComponent>
        </div>
        <div class="button-column">
          <ButtonComponent></ButtonComponent>
        </div>
        <div class="button-column">
          <ButtonComponent></ButtonComponent>
        </div>
      </div>
      <!--JOystick-->
      <div class="col-3">
        <div class="joystick-column">
          <JoystickComponent
            ref="JoystickComponentRef"
            v:bind:usuario="usuario"
          ></JoystickComponent>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "App",
  components: {
    MapComponent,
    RobotConfigComponent,
    ButtonComponent,
    JoystickComponent,
    LogsComponent,
    ParamsComponent,
    CallServiceComponent,
  },

  methods: {
    connect_ros(ros) {
      console.log("Evento de conexion recibido");
      this.$refs.MapComponentRef.setMapViewer(ros);
      this.$refs.MapComponentRef.amclPose(ros);
      this.$refs.JoystickComponentRef.joystickConfig(ros);
      this.$refs.LogsComponentRef.logsInit();
      this.$refs.ParamsComponentRef.paramInit(ros);
      this.$refs.ButtonInitLocComponentRef.buttonInit(ros);
      this.$refs.ButtonFindShelfComponentRef.buttonInit(ros);
    },
    config_web_event(config_web) {
      console.log("[Params component] event function");
      this.$refs.JoystickComponentRef.paramConfig(config_web);
      console.log("[config_web_event]");
      console.log(config_web);
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  height: 100vh; /* Use the full height of the viewport */
}

.config-column {
  flex: 0 0 20%; /* 20% of the width */
  padding: 1px; /* Optional: add some padding */
  box-sizing: border-box;
}

.map-column {
  flex: 0 0 40%; /* 40% of the width */
  padding: 10px; /* Optional: add some padding */
  box-sizing: border-box;
}
.button-column {
  flex: 0 0 20%; /* 40% of the width */
  padding: 10px; /* Optional: add some padding */
  box-sizing: border-box;
}
.joystick-column {
  flex: 0 0 20%; /* 40% of the width */
  padding: 10px; /* Optional: add some padding */
  box-sizing: border-box;
}
.app-container {
  margin-top: 20px; /* Adjust the top margin as needed */
  margin-bottom: 20px; /* Adjust the bottom margin as needed */
}

.button-container {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: calc(
    100vh - 40px
  ); /* Adjust this height to account for the margins */
}

.button-column {
  display: flex;

  justify-content: center; /* Center the buttons horizontally if needed */
}

.button-column > * {
  flex: 0 0 15%; /* Make each button take up a portion of the container height */
}
</style>
