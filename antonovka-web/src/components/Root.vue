<template>
  <div>
    <div id="results">
      <div class="element">
        <div class="button-wrapper">
          <div class="button"><font-awesome-icon icon="plus" /></div>
          <input type="file" id="file" ref="file" v-on:change="upload()" />
        </div>
        <div class="meta" style="visibility: hidden">
          <div class="meta-element">
            <div class="meta-header">Время:</div>
          </div>
          <div class="meta-element">
            <div class="meta-header">Координаты:</div>
            <input class="meta-input" />
          </div>
          <div class="meta-element">
            <div class="meta-header">Комментарии:</div>
            <input class="meta-input" />
          </div>
        </div>
      </div>
      <div
        v-for="task in tasks.slice().reverse()"
        :key="task.taskId"
        class="element"
      >
        <v-popover
          offset="16"
          :disabled="isHeatmapDisabled(task.heatmapUrl)"
          class="heatmap-popover"
        >
          <div
            class="image tooltip-target b3"
            v-tooltip="{ content: tooltip(task.result) }"
            :style="{
              backgroundImage: 'url(' + task.imageUrl + ')',
              borderColor: borderColor(task.result),
              opacity: imageOpacity(task.result),
            }"
          >
            <div class="spinner-wrapper">
              <div
                class="spinner"
                :style="{
                  visibility: task.result == null ? 'visible' : 'hidden',
                }"
              ></div>
            </div>
          </div>
          <template slot="popover">
            <div
              class="image-heatmap"
              :style="{
                backgroundImage: 'url(' + task.heatmapUrl + ')',
              }"
            ></div>
          </template>
        </v-popover>
        <div class="meta">
          <div class="meta-element">
            <div class="meta-header">Время:</div>
            {{ task.datetime }}
          </div>
          <div class="meta-element">
            <div class="meta-header">Координаты:</div>
            <input
              v-model="task.location"
              class="meta-input"
              :style="{
                borderBottom:
                  task.location == '' ? '1px solid' : '1px solid transparent',
              }"
            />
          </div>
          <div class="meta-element">
            <div class="meta-header">Комментарии:</div>
            <input
              v-model="task.comment"
              class="meta-input"
              :style="{
                borderBottom:
                  task.comment == '' ? '1px solid' : '1px solid transparent',
              }"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const url = "http://77.223.104.98:5000/api";

class Task {
  constructor(taskId, imageUrl, datetime) {
    this.taskId = taskId;
    this.imageUrl = imageUrl;
    this.datetime = datetime;
    this.result = null;
    this.location = "";
    this.comment = "";
    this.heatmapUrl = "";
  }
}

export default {
  data() {
    return {
      tasks: [],
    };
  },
  methods: {
    upload: function() {
      this.file = this.$refs.file.files[0];
      let formData = new FormData();
      formData.append("file", this.file);
      this.$refs.file.value = null;
      axios
        .post(`${url}/predict`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          let imageUrl = `${url}/image/${response.data.filename}`;
          const today = new Date(Date.now());
          this.tasks.push(
            new Task(
              response.data.task_id,
              imageUrl,
              this.getCurrentDate(today, "dd.mm.yyyy hh:MM")
            )
          );
          setTimeout(
            (taskId) => this.getTaskResult(taskId),
            1000,
            response.data.task_id
          );
        });
    },

    getTaskResult: function(taskId) {
      axios.get(`${url}/${taskId}/status`).then((response) => {
        if (response.data.result != "") {
          let task = this.tasks.find((value) => value.taskId == taskId);
          task.result = response.data.result;
          if (response.data.heatmap != "") {
            task.heatmapUrl = `${url}/image/${response.data.heatmap}`;
          }
        } else {
          setTimeout((taskId) => this.getTaskResult(taskId), 1000, taskId);
        }
      });
    },

    borderColor: function(taskResult) {
      if (taskResult == null) {
        return "gray";
      }
      if (taskResult == "true") {
        return "#EA2027";
      }
      return "#70B17F";
    },

    imageOpacity: function(taskResult) {
      return taskResult == null ? 0.5 : 1;
    },

    tooltip: function(taskResult) {
      if (taskResult == "false") {
        return "Яблоня здорова!";
      }
      if (taskResult == "true") {
        return "Яблоня больна :(";
      }
    },

    getCurrentDate: function(date, format) {
      function pad(num, size) {
        var s = "00" + num;
        return s.substr(s.length - size);
      }
      const map = {
        mm: date.getMonth() + 1,
        dd: date.getDate(),
        yy: date
          .getFullYear()
          .toString()
          .slice(-2),
        yyyy: date.getFullYear(),
        hh: pad(date.getHours(), 2),
        MM: pad(date.getMinutes(), 2),
      };

      return format.replace(/mm|dd|yy|hh|MM|yyy/gi, (matched) => map[matched]);
    },

    isHeatmapDisabled: function(heatmapUrl) {
      if (heatmapUrl == "") {
        return true;
      }
      return false;
    },
  },
};
</script>

<style>
#results {
  font-size: 2em;
  width: 70%;
  min-width: 20em;
  margin: 2em auto;
}

.image {
  width: 200px;
  height: 200px;
  border: 5px solid;
  background-position: center center;
  background-size: cover;
  box-shadow: 0px 0px 33px -7px rgb(94, 94, 94, 0.5);
}

.image-heatmap {
  background: #ffffff;
  width: 300px;
  height: 300px;
  background-position: center center;
  background-size: cover;
  box-shadow: 0px 0px 33px -7px rgb(94, 94, 94, 0.5);
}

.element {
  display: inline-block;
  margin: 20px;
}

.heatmap-popover {
  height: 210px;
}

.meta {
  margin-top: 10px;
  font-size: 13px;
  color: #37474f;
  text-align: left;
  width: 210px;
  margin-top: 10px;
  height: 80px;
}

.meta-element {
  display: flex;
  align-content: flex-start;
  margin: 5px 0;
}

.meta-header {
  margin-right: 3px;
  border-bottom: 1px solid transparent;
}

.meta-input {
  width: 100%;
  font-family: inherit;
  font-size: 13px;
  color: #37474f;
  margin-top: -1px;
  background: None;
  border: 0;
  border-bottom: 1px solid black;
}

.meta-input:focus {
  background: None;
  outline: none;
  border: 0;
  border-bottom: 1px solid red;
}

.button-wrapper {
  width: 200px;
  height: 200px;
  border: 5px rgba(150, 155, 163, 0.4) dashed;
  background-position: center center;
  background-size: cover;
  position: relative;
  overflow: hidden;
  box-shadow: 0px 0px 33px -7px rgb(94, 94, 94, 0.5);
}

.button {
  padding: 25px 20px;
  border: 0;
  font-size: 100px;
  color: rgba(150, 155, 163, 0.7);
}

.button-wrapper input[type="file"] {
  height: 200px;
  font-size: 100px;
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
}

.spinner-wrapper {
}

.spinner {
  margin: 30% auto;
  height: 60px;
  width: 60px;
  -webkit-animation: rotation 0.6s infinite linear;
  -moz-animation: rotation 0.6s infinite linear;
  -o-animation: rotation 0.6s infinite linear;
  animation: rotation 0.6s infinite linear;
  border-left: 6px solid rgba(0, 174, 239, 0.15);
  border-right: 6px solid rgba(0, 174, 239, 0.15);
  border-bottom: 6px solid rgba(0, 174, 239, 0.15);
  border-top: 6px solid rgba(0, 174, 239, 1);
  border-radius: 100%;
}

@-webkit-keyframes rotation {
  from {
    -webkit-transform: rotate(0deg);
  }
  to {
    -webkit-transform: rotate(359deg);
  }
}
@-moz-keyframes rotation {
  from {
    -moz-transform: rotate(0deg);
  }
  to {
    -moz-transform: rotate(359deg);
  }
}
@-o-keyframes rotation {
  from {
    -o-transform: rotate(0deg);
  }
  to {
    -o-transform: rotate(359deg);
  }
}
@keyframes rotation {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(359deg);
  }
}

.tooltip {
  display: block !important;
  z-index: 10000;
}

.tooltip .tooltip-inner {
  background: #576574;
  color: white;
  border-radius: 10px;
  padding: 5px 10px 7px;
}

.tooltip .tooltip-arrow {
  width: 0;
  height: 0;
  border-style: solid;
  position: absolute;
  margin: 5px;
  border-color: #576574;
  z-index: 1;
}

.tooltip[x-placement^="top"] {
  margin-bottom: 5px;
}

.tooltip[x-placement^="top"] .tooltip-arrow {
  border-width: 5px 5px 0 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  bottom: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}

.tooltip[x-placement^="bottom"] {
  margin-top: 5px;
}

.tooltip[x-placement^="bottom"] .tooltip-arrow {
  border-width: 0 5px 5px 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-top-color: transparent !important;
  top: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}

.tooltip[x-placement^="right"] {
  margin-left: 5px;
}

.tooltip[x-placement^="right"] .tooltip-arrow {
  border-width: 5px 5px 5px 0;
  border-left-color: transparent !important;
  border-top-color: transparent !important;
  border-bottom-color: transparent !important;
  left: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}

.tooltip[x-placement^="left"] {
  margin-right: 5px;
}

.tooltip[x-placement^="left"] .tooltip-arrow {
  border-width: 5px 0 5px 5px;
  border-top-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  right: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}

.tooltip.popover .popover-inner {
  background: #f9f9f9;
  border: 0;
  color: black;
  border-radius: 0;
  box-shadow: 0px 0px 33px -7px #1e272e;
  padding: 0 !important;
}

.tooltip.popover .popover-arrow {
  border-color: #f9f9f9;
}

.tooltip[aria-hidden="true"] {
  visibility: hidden;
  opacity: 0;
  transition: opacity 0.15s, visibility 0.15s;
}

.tooltip[aria-hidden="false"] {
  visibility: visible;
  opacity: 1;
  transition: opacity 0.15s;
}
</style>
