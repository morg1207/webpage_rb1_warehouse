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
    <div class="row"> <!-- Añadido margen superior -->
      <div class="col-2 text-center custom-colum">
        <!-- Connect-->
        <div class="card mt-2  custom-card mb-3">
          <RobotConfigComponent @my-event="connect_ros" @my-event-error-conection="error_conection" @my-event-disconnect= "disconnect">

          </RobotConfigComponent>
        </div>

        <!--Log-->
        <div class="card mt-2  custom-card mb-3">
          <LogsComponent
            ref="LogsComponentRef"
            v:bind:usuario="usuario"
          ></LogsComponent>
        </div>
        <!-- Load file-->
        <div class="card mt-2  custom-card mb-3">
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
        <div class="button-column  custom-card mb-3">
          <CallServiceComponent
          @my-event-call-service="call_service"
          ref="ButtonInitCallServiceRef"
          v:bind:usuario="usuario">
        </CallServiceComponent>
        </div>

      </div>
      <!--Botones-->
      <div class="col-2 button-container">
        <div class="button-column  custom-card mb-3">
          <ButtonComponent
            ref="ButtonInitLocComponentRef"
            v:bind:usuario="usuario"
            :initialState="'inactive'"
            :buttonTextActive="'Init Localization'"
            :buttonTextInactive="'Deactivated'"
            :buttonTextProcessing="'Localizando robot...'"
            :buttonPublishBT="'find_station_and_init_local'"
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
          <ButtonComponent
            ref="ButtonApproachAndPickShelfComponentRef"
            v:bind:usuario="usuario"
            :initialState="'inactive'"
            :buttonTextActive="'Approach and pick shelf'"
            :buttonTextInactive="'Deactivated'"
            :buttonTextProcessing="'Approach shelf...'"
            :buttonPublishBT="'approach_and_pick_shelf'"
          ></ButtonComponent>
        </div>
        <div class="button-column  custom-card mb-3">
          <ButtonComponent
            ref="ButtonCarryAndDischargeShelfComponentRef"
            v:bind:usuario="usuario"
            :initialState="'inactive'"
            :buttonTextActive="'Carry and discharge shelf'"
            :buttonTextInactive="'Deactivated'"
            :buttonTextProcessing="'Delivery shelf...'"
            :buttonPublishBT="'carry_and_discharge_shelf'"
          ></ButtonComponent>
        </div>
        <div class="button-column  custom-card mb-3 ">
          <ButtonComponent
            ref="ButtonExecuteAllTasksComponentRef"
            v:bind:usuario="usuario"
            :initialState="'inactive'"
            :buttonTextActive="'Executed all tasks'"
            :buttonTextInactive="'Deactivated'"
            :buttonTextProcessing="'Completing all tasks...'"
            :buttonPublishBT="'behaviortree_entire'"
          ></ButtonComponent>
        </div>
      </div>
      <!-- Joystick -->
      <div class="col-2 joystick-column">
        <div class="custom-card w-100 d-flex justify-content-center align-items-center">
          <JoystickComponent ref="JoystickComponentRef" v-bind:usuario="usuario"></JoystickComponent>
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
    call_service(){
      this.$refs.ButtonInitLocComponentRef.buttonInit(ros);
      this.$refs.ButtonFindShelfComponentRef.buttonInit(ros);
      this.$refs.ButtonApproachAndPickShelfComponentRef.buttonInit(ros);
      this.$refs.ButtonCarryAndDischargeShelfComponentRef.buttonInit(ros);
      this.$refs.ButtonCarryAndDischargeShelfComponentRef.buttonShowSubButtons(ros);
      this.$refs.ButtonExecuteAllTasksComponentRef.buttonInit(ros);

    },
    connect_ros(ros,webpage_adress) {
      console.log("Evento de conexion recibido");
      this.$refs.MapComponentRef.setMapViewer(ros);
      this.$refs.MapComponentRef.amclPose(ros);
      this.$refs.MapComponentRef.shelfPose(ros);
      this.$refs.JoystickComponentRef.joystickConfig(ros);
      this.$refs.LogsComponentRef.logsInit();
      this.$refs.ParamsComponentRef.paramInit(ros);
      this.$refs.ButtonInitCallServiceRef.callServiceInit(webpage_adress);
    },
    error_conection(){
      this.$refs.LogsComponentRef.logsErrorConection();
    },
    disconnect(){
      this.$refs.LogsComponentRef.logsDisconnect();
      //close button
      this.$refs.ButtonInitLocComponentRef.buttonClose();
      this.$refs.ButtonFindShelfComponentRef.buttonClose();
      this.$refs.ButtonApproachAndPickShelfComponentRef.buttonClose();
      this.$refs.ButtonCarryAndDischargeShelfComponentRef.buttonClose();
      this.$refs.ButtonCarryAndDischargeShelfComponentRef.buttonClose()
      this.$refs.ButtonExecuteAllTasksComponentRef.buttonClose();
      this.$refs.MapComponentRef.mapClose();
      this.$refs.JoystickComponentRef.joystickClose();
      this.$refs.ButtonInitCallServiceRef.callServiceClose();

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

