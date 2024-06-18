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
  <div id="app" class="container-fluid app-background">
    <div class="row">
      <div class="col-2 text-center">
        <!-- Connect-->
        <div class="card mt-2  custom-card">
          <RobotConfigComponent @my-event="connect_ros"></RobotConfigComponent>
        </div>

        <!--Log-->
        <div class="card mt-2  custom-card">
          <LogsComponent
            ref="LogsComponentRef"
            v:bind:usuario="usuario"
          ></LogsComponent>
        </div>
        <!-- Load file-->
        <div class="card mt-2  custom-card">
          <ParamsComponent
            @event_config_web="config_web_event"
            ref="ParamsComponentRef"
            v:bind:usuario="usuario"
          ></ParamsComponent>
        </div>
      </div>
      <!--Map-->
      <div class="col-6" style="overflow: auto">
        <div class="map-column  custom-card">
          <MapComponent
            ref="MapComponentRef"
            v:bind:usuario="usuario"
          ></MapComponent>
        </div>
      </div>
      <!--Botones-->
      <div class="col-2.0 button-container">
        <div class="button-column  custom-card mb-3">
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
        <div class="button-column  custom-card mb-3">
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
        <div class="button-column  custom-card mb-3">
          <ButtonComponent></ButtonComponent>
        </div>
        <div class="button-column  custom-card mb-3">
          <ButtonComponent></ButtonComponent>
        </div>
        <div class="button-column  custom-card mb-3 ">
          <ButtonComponent></ButtonComponent>
        </div>
      </div>
      <!--JOystick-->
      <div class="col-2.0">
        <div class="joystick-column w-100  custom-card">
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
      this.$refs.MapComponentRef.shelfPose(ros);
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

