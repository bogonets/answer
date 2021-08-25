<template>
  <v-card id="main-detail" :style="this.$backgroundColor()">
    <!-- 설정 텍스트 + info 버튼 -->
    <v-card-title style="margin: 0; padding: 0;">
      <v-toolbar height="24">
        <span>{{ $t("setting") }}</span>
        <v-spacer v-if="lambdaNtask && lambdaNtask.info"></v-spacer>
        <v-btn
          v-if="lambdaNtask && lambdaNtask.info"
          small
          icon
          style="margin: 0px;"
          :style="this.$buttonColor()"
          @click="showInformation = true"
        >
          <v-icon>info</v-icon>
        </v-btn>
      </v-toolbar>
    </v-card-title>
    <v-dialog
      v-model="showInformation"
      scrollable
      max-width="650px"
      transition="dialog-transition"
    >
      <!-- 람다 이름 -->
      <lambda-info-viewer
        v-if="showInformation"
        :infos="lambdaNtask.info"
        @onClose="showInformation = false"
      ></lambda-info-viewer>
    </v-dialog>

    <!-- 속성값 시작 -->
    <v-card-text
      style="position: absolute; top: 24px; height: calc(100% - 64px); overflow: auto;"
    >
      <!-- Task & Lambda 이름 -->
      <template v-if="title !== null || title !== undefined">
        <v-layout row wrap style="margin: 0; margin-top: 5px;">
          <v-flex xs11 @dblclick="onEditTitle">
            <span v-if="!editTitle" style="font-size: 18px;">{{ title }}</span>
            <input
              v-else
              type="text"
              v-model="title"
              ref="title"
              id="title"
              @input="onChangeProperty($event, 'v-text-field')"
              style="width: 100%; font-size: 18px;"
            />
          </v-flex>
          <v-flex xs1>
            <v-icon size="15" ref="titleEditor" @click="onEditTitle"
              >edit</v-icon
            >
          </v-flex>
        </v-layout>
        <v-layout v-if="uid !== null && uid !== undefined && uid.length !== 0">
          <v-text-field
            label="uid"
            v-model="uid"
            dense
            outlined
            hide-details
            type="text"
            style="margin-top: 10px;"
            @input="onChangeProperty($event, null)"
          ></v-text-field>
        </v-layout>
        <v-divider></v-divider>
      </template>

      <!-- 속성설정 -->
      <div v-if="ui_setting" class="title">
        <v-card-actions
          @click="onOpenPropertiesSetting"
          style="cursor: pointer;"
        >
          <span id="sub_title">
            {{ $t("properties") + " " + $t("setting") }}
          </span>
          <v-spacer></v-spacer>
          <v-btn
            :style="this.$buttonColor()"
            icon
            fab
            small
            style="width: 20px; height: 20px; margin: 0px;"
          >
            <v-icon size="20">{{
              show_properties ? "arrow_drop_up" : "arrow_drop_down"
            }}</v-icon>
          </v-btn>
        </v-card-actions>
        <hr />
      </div>
      <transition name="fade">
        <v-card-text v-if="show_properties" ref="property_zone">
          <template v-for="(ui, index) in ui_setting">
            <v-text-field
              v-if="
                checkRule(ui.rule) &&
                  !ui.valid.advance &&
                  ui.component.name === 'v-text-field'
              "
              :disabled="ruleIsReadonly(ui.rule)"
              :key="index"
              :class="ui.component.class"
              :ref="ui.name"
              :id="ui.name"
              :label="ui.component.label"
              :type="ui.component.type"
              :min="ui.component.valid.min"
              :max="ui.component.valid.max"
              :step="ui.component.valid.step"
              :title="getHelp(ui.help)"
              v-model="ui.component.value"
              @input="onChangeProperty($event, ui.component.name)"
              dense
              outlined
            ></v-text-field>

            <div
              v-else-if="
                checkRule(ui.rule) &&
                  !ui.valid.advance &&
                  ui.component.name === 'v-select'
              "
              :key="index"
              :title="getHelp(ui.help)"
            >
              <v-select
                :disabled="ruleIsReadonly(ui.rule)"
                :class="ui.component.class"
                :ref="ui.name"
                :id="ui.name"
                :label="ui.component.label"
                :items="ui.component.valid.items"
                v-model="ui.component.value"
                @change="onChangeProperty($event)"
                hide-selected
                dense
                outlined
              ></v-select>
            </div>

            <div
              v-else-if="
                checkRule(ui.rule) &&
                  !ui.valid.advance &&
                  ui.component.name === 'v-checkbox'
              "
              :title="getHelp(ui.help)"
              style="margin-bottom: 22px;"
              :key="index"
            >
              <v-checkbox
                :disabled="ruleIsReadonly(ui.rule)"
                :class="ui.component.class"
                :ref="ui.name"
                :id="ui.name"
                :label="ui.component.label"
                v-model="ui.component.value"
                hide-details
                @change="onChangeProperty($event)"
              ></v-checkbox>
            </div>

            <v-jupyter-select
              v-else-if="
                checkRule(ui.rule) &&
                  !ui.valid.advance &&
                  ui.component.name === 'v-jupyter-select'
              "
              :disabled="ruleIsReadonly(ui.rule)"
              :key="index"
              :ref="ui.name"
              :id="ui.name"
              :label="ui.component.label"
              :taskName="taskOfLambda"
              :lambdaType="type.split('/')[1]"
              :propName="ui.component.label"
              :title="getHelp(ui.help)"
              v-model="ui.component.value"
              @input="onChangeProperty($event)"
              dense
              outline
            ></v-jupyter-select>

            <a-color-picker
              v-else-if="
                checkRule(ui.rule) &&
                  !ui.valid.advance &&
                  ui.component.name === 'a-color-picker'
              "
              :disabled="ruleIsReadonly(ui.rule)"
              :key="index"
              :ref="ui.name"
              :id="ui.name"
              :label="ui.component.label"
              :resultRgbformat="ui.component.valid.rgb"
              :class="ui.component.class"
              :title="getHelp(ui.help)"
              v-model="ui.component.value"
              @input="onChangeProperty($event)"
              dense
              outline
            ></a-color-picker>

            <v-csv-field
              v-else-if="
                checkRule(ui.rule) &&
                  !ui.valid.advance &&
                  ui.component.name === 'v-csv-field'
              "
              :disabled="ruleIsReadonly(ui.rule)"
              :key="index"
              :ref="ui.name"
              :id="ui.name"
              :label="ui.component.label"
              :items="ui.component.valid.items"
              :title="getHelp(ui.help)"
              v-model="ui.component.value"
              @input="onChangeProperty($event)"
              style="margin-bottom: 22px;"
              dense
              outline
            ></v-csv-field>

            <a-csv-input
              v-else-if="
                checkRule(ui.rule) &&
                  !ui.valid.advance &&
                  ui.component.name === 'a-csv-input'
              "
              :disabled="ruleIsReadonly(ui.rule)"
              :key="index"
              :ref="ui.name"
              :id="ui.name"
              :label="ui.component.label"
              :title="getHelp(ui.help)"
              v-model="ui.component.value"
              @input="onChangeProperty($event)"
              style="margin-bottom: 22px;"
              dense
              outlined
            ></a-csv-input>
            <v-btn
              :style="this.$buttonColor()"
              v-else-if="
                ui.rule === 'read_and_write' &&
                  !ui.valid.advance &&
                  ui.component.name === 'v-btn'
              "
              :disabled="ruleIsReadonly(ui.rule)"
              :key="index"
              :ref="ui.name"
              :id="ui.name"
              :title="getHelp(ui.help)"
              class="roi_setting"
              style="width: 100%;"
              >{{ ui.component.label }}</v-btn
            >
          </template>
          <v-btn
            v-if="metaComponent"
            :id="metaComponent.name"
            :style="this.$buttonColor()"
            @click="showPropertyWidget()"
            class="roi_setting"
            style="width: 100%;"
            >{{ metaComponent.name }}</v-btn
          >
        </v-card-text>
      </transition>

      <!-- 상세설정 -->
      <div v-if="ui_setting && advance" class="title">
        <v-card-actions @click="onOpenDetailSetting" style="cursor: pointer;">
          <span id="sub_title">
            {{ $t("detail_setting") }}
          </span>
          <v-spacer></v-spacer>
          <v-btn
            :style="this.$buttonColor()"
            icon
            fab
            small
            style="width: 20px; height: 20px; margin: 0px;"
          >
            <v-icon size="20">{{
              show_details ? "arrow_drop_up" : "arrow_drop_down"
            }}</v-icon>
          </v-btn>
        </v-card-actions>
        <hr />
      </div>
      <transition name="fade">
        <v-card-text v-if="show_details" ref="property_zone">
          <template v-for="(ui, index) in ui_setting">
            <v-text-field
              v-if="
                checkRule(ui.rule) &&
                  ui.valid.advance &&
                  ui.component.name === 'v-text-field'
              "
              :disabled="ruleIsReadonly(ui.rule)"
              :key="index"
              :class="ui.component.class"
              :ref="ui.name"
              :id="ui.name"
              :label="ui.component.label"
              :type="ui.component.type"
              :min="ui.component.valid.min"
              :max="ui.component.valid.max"
              :step="ui.component.valid.step"
              :title="getHelp(ui.help)"
              v-model="ui.component.value"
              @input="onChangeProperty($event, ui.component.name)"
              dense
              outlined
            ></v-text-field>

            <div
              v-else-if="
                checkRule(ui.rule) &&
                  ui.valid.advance &&
                  ui.component.name === 'v-select'
              "
              :key="index"
              :title="getHelp(ui.help)"
            >
              <v-select
                :disabled="ruleIsReadonly(ui.rule)"
                :class="ui.component.class"
                :ref="ui.name"
                :id="ui.name"
                :label="ui.component.label"
                :items="ui.component.valid.items"
                v-model="ui.component.value"
                @change="onChangeProperty($event)"
                hide-selected
                dense
                outlined
              ></v-select>
            </div>

            <div
              v-else-if="
                checkRule(ui.rule) &&
                  ui.valid.advance &&
                  ui.component.name === 'v-checkbox'
              "
              :title="getHelp(ui.help)"
              style="margin-bottom: 22px;"
              :key="index"
            >
              <v-checkbox
                :disabled="ruleIsReadonly(ui.rule)"
                :class="ui.component.class"
                :ref="ui.name"
                :id="ui.name"
                :label="ui.component.label"
                v-model="ui.component.value"
                hide-details
                @change="onChangeProperty($event)"
              ></v-checkbox>
            </div>

            <v-jupyter-select
              v-else-if="
                checkRule(ui.rule) &&
                  ui.valid.advance &&
                  ui.component.name === 'v-jupyter-select'
              "
              :disabled="ruleIsReadonly(ui.rule)"
              :key="index"
              :ref="ui.name"
              :id="ui.name"
              :label="ui.component.label"
              :taskName="taskOfLambda"
              :lambdaType="type.split('/')[1]"
              :propName="ui.component.label"
              :title="getHelp(ui.help)"
              v-model="ui.component.value"
              @input="onChangeProperty($event)"
              dense
              outline
            ></v-jupyter-select>

            <a-color-picker
              v-else-if="
                checkRule(ui.rule) &&
                  ui.valid.advance &&
                  ui.component.name === 'a-color-picker'
              "
              :disabled="ruleIsReadonly(ui.rule)"
              :key="index"
              :ref="ui.name"
              :id="ui.name"
              :label="ui.component.label"
              :resultRgbformat="ui.component.valid.rgb"
              :class="ui.component.class"
              :title="getHelp(ui.help)"
              v-model="ui.component.value"
              @input="onChangeProperty($event)"
              dense
              outline
            ></a-color-picker>

            <v-csv-field
              v-else-if="
                checkRule(ui.rule) &&
                  ui.valid.advance &&
                  ui.component.name === 'v-csv-field'
              "
              :disabled="ruleIsReadonly(ui.rule)"
              :key="index"
              :ref="ui.name"
              :id="ui.name"
              :label="ui.component.label"
              :items="ui.component.valid.items"
              :title="getHelp(ui.help)"
              v-model="ui.component.value"
              @input="onChangeProperty($event)"
              style="margin-bottom: 22px;"
              dense
              outline
            ></v-csv-field>

            <a-csv-input
              v-else-if="
                checkRule(ui.rule) &&
                  ui.valid.advance &&
                  ui.component.name === 'a-csv-input'
              "
              :disabled="ruleIsReadonly(ui.rule)"
              :key="index"
              :ref="ui.name"
              :id="ui.name"
              :label="ui.component.label"
              :title="getHelp(ui.help)"
              v-model="ui.component.value"
              @input="onChangeProperty($event)"
              style="margin-bottom: 22px;"
              dense
              outlined
            ></a-csv-input>
            <v-btn
              :style="this.$buttonColor()"
              v-else-if="
                ui.rule === 'read_and_write' &&
                  ui.valid.advance &&
                  ui.component.name === 'v-btn'
              "
              :disabled="ruleIsReadonly(ui.rule)"
              :key="index"
              :ref="ui.name"
              :id="ui.name"
              :title="getHelp(ui.help)"
              class="roi_setting"
              style="width: 100%;"
              >{{ ui.component.label }}</v-btn
            >
          </template>
          <v-btn
            :style="this.$buttonColor()"
            v-if="metaComponent"
            :id="metaComponent.name"
            @click="showPropertyWidget()"
            class="roi_setting"
            style="width: 100%;"
            >{{ metaComponent.name }}</v-btn
          >
        </v-card-text>
      </transition>

      <!-- 입력설정 -->
      <div v-if="inputs.length !== 0 || dynamicInputSlot" class="title">
        <v-card-actions
          @click="onOpenInputSlotSetting"
          style="cursor: pointer;"
        >
          <span id="sub_title">
            {{ $t("input") + " " + $t("slot") + " " + $t("setting") }}
          </span>
          <v-spacer></v-spacer>
          <v-btn
            :style="this.$buttonColor()"
            icon
            fab
            small
            style="width: 20px; height: 20px; margin: 0px;"
          >
            <v-icon size="20">
              {{ show_inputs ? "arrow_drop_up" : "arrow_drop_down" }}
            </v-icon>
          </v-btn>
        </v-card-actions>
        <hr />
      </div>
      <transition name="fade">
        <v-card-text v-if="show_inputs">
          <v-btn
            :style="this.$buttonColor()"
            v-if="dynamicInputSlot"
            style="width: 100%; margin: 0; margin-bottom: 10px;"
            small
            @click="onAddInputSlot"
            >{{ $t("add") }}</v-btn
          >
          <v-expansion-panels focusable v-model="expansionInputPanel">
            <v-expansion-panel
              v-for="(input, index) in inputs"
              :key="index"
              class="elevation-5"
            >
              <v-expansion-panel-header
                :disable-icon-rotate="!dynamicInputSlot"
              >
                {{ input.name ? input.name : $t("detailsetting.setname") }}
                <template
                  v-if="dynamicInputSlot && !input.readonly"
                  v-slot:actions
                >
                  <v-menu
                    :dark="this.$vuetify.theme.dark"
                    offset-y
                    offset-x
                    top
                    left
                  >
                    <template v-slot:activator="{ on }">
                      <v-icon
                        v-on="on"
                        size="20"
                        style="cursor: pointer"
                        color="error"
                        @click.stop
                        :title="$t('delete')"
                        >remove_circle</v-icon
                      >
                    </template>
                    <v-card
                      style="max-width: 280px; border: 1px solid; border-radius: 20px 20px 0px 20px !important;"
                    >
                      <div class="menu-title">
                        <v-icon color="warning">warning</v-icon>&nbsp;&nbsp;
                        <strong>{{ $t("warning") }}</strong>
                      </div>
                      <v-divider></v-divider>
                      <v-card-text>
                        <div>
                          <span>{{ $t("connection_will_disconnected") }}</span>
                        </div>
                        <div>
                          <span>{{ $t("dialog_message.delete") }}</span>
                        </div>
                      </v-card-text>
                      <v-divider></v-divider>
                      <v-card-actions>
                        <v-btn :style="this.$buttonColor()" small>{{
                          $t("cancel")
                        }}</v-btn>
                        <v-spacer></v-spacer>
                        <v-btn
                          :style="this.$buttonColor()"
                          small
                          @click="onDeleteInputSlot(index)"
                        >
                          {{ $t("continue") }}
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-menu>
                </template>
                <template v-else v-slot:actions>
                  <v-tooltip bottom open-delay="1000">
                    <template v-slot:activator="{ on }">
                      <v-icon v-on="on" size="20" style="cursor: pointer"
                        >arrow_drop_down</v-icon
                      >
                    </template>
                    <span>{{ $t("open") }}</span>
                  </v-tooltip>
                </template>
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-card-text>
                  <v-text-field
                    :disabled="input.readonly"
                    :label="$t('name') + ' ' + $t('setting')"
                    :placeholder="$t('detailsetting.setname')"
                    :error="
                      input.name === null ||
                        input.name === undefined ||
                        input.name === ''
                    "
                    @input="onChangeProperty($event, 'v-text-field')"
                    v-model="input.name"
                    dense
                    outlined
                    hide-details
                    type="text"
                    ref="inputSlotText"
                    style="margin-bottom: 10px;"
                  ></v-text-field>
                </v-card-text>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-card-text>
      </transition>

      <div v-if="outputs.length !== 0 || dynamicOutputSlot" class="title">
        <v-card-actions
          @click="onOpenOutputSlotSetting"
          style="cursor: pointer;"
        >
          <span id="sub_title">{{
            $t("output") + " " + $t("slot") + " " + $t("setting")
          }}</span>
          <v-spacer></v-spacer>
          <v-btn
            :style="this.$buttonColor()"
            icon
            fab
            small
            style="width: 20px; height: 20px; margin: 0px;"
          >
            <v-icon size="20">{{
              show_outputs ? "arrow_drop_up" : "arrow_drop_down"
            }}</v-icon>
          </v-btn>
        </v-card-actions>
        <hr />
      </div>
      <transition name="fade">
        <v-card-text v-if="show_outputs">
          <v-btn
            :style="this.$buttonColor()"
            v-if="dynamicOutputSlot"
            style="width: 100%; margin: 0; margin-bottom: 10px;"
            small
            @click="onAddOutputSlot"
            >{{ $t("add") }}</v-btn
          >
          <v-expansion-panels focusable v-model="expansionOutputPanel">
            <v-expansion-panel
              v-for="(output, index) in outputs"
              :key="index"
              class="elevation-5"
            >
              <v-expansion-panel-header
                :disable-icon-rotate="!dynamicOutputSlot"
              >
                {{ output.name ? output.name : $t("detailsetting.setname") }}
                <template
                  v-if="dynamicOutputSlot && !output.readonly"
                  v-slot:actions
                >
                  <v-menu
                    :dark="this.$vuetify.theme.dark"
                    offset-x
                    offset-y
                    top
                    left
                  >
                    <template v-slot:activator="{ on }">
                      <v-icon
                        v-on="on"
                        size="20"
                        style="cursor: pointer"
                        color="error"
                        @click.stop
                        :title="$t('delete')"
                        >remove_circle</v-icon
                      >
                    </template>
                    <v-card
                      style="max-width: 280px; border: 1px solid; border-radius: 20px 20px 0px 20px !important;"
                    >
                      <div class="menu-title">
                        <v-icon color="warning">warning</v-icon>&nbsp;&nbsp;
                        <strong>{{ $t("warning") }}</strong>
                      </div>
                      <v-divider></v-divider>
                      <v-card-text>
                        <div>
                          <span>{{ $t("connection_will_disconnected") }}</span>
                        </div>
                        <div>
                          <span>{{ $t("dialog_message.delete") }}</span>
                        </div>
                      </v-card-text>
                      <v-divider></v-divider>
                      <v-card-actions>
                        <v-btn :style="this.$buttonColor()" small>{{
                          $t("cancel")
                        }}</v-btn>
                        <v-spacer></v-spacer>
                        <v-btn
                          :style="this.$buttonColor()"
                          small
                          @click="onDeleteOutputSlot(index)"
                          >{{ $t("continue") }}</v-btn
                        >
                      </v-card-actions>
                    </v-card>
                  </v-menu>
                </template>
                <template v-else v-slot:actions>
                  <v-tooltip bottom open-delay="1000">
                    <template v-slot:activator="{ on }">
                      <v-icon v-on="on" size="20" style="cursor: pointer"
                        >arrow_drop_down</v-icon
                      >
                    </template>
                    <span>{{ $t("open") }}</span>
                  </v-tooltip>
                </template>
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-card-text>
                  <v-text-field
                    :disabled="output.readonly"
                    :label="$t('name') + ' ' + $t('setting')"
                    :error="
                      output.name === null ||
                        output.name === undefined ||
                        output.name === ''
                    "
                    :placeholder="$t('detailsetting.setname')"
                    @input="onChangeProperty($event, 'v-text-field')"
                    v-model="output.name"
                    dense
                    outlined
                    hide-details
                    type="text"
                    ref="outputSlotText"
                    style="margin-bottom: 10px;"
                  ></v-text-field>
                </v-card-text>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-card-text>
      </transition>

      <!--
      <div v-if="ui_signals !== null || ui_signals !== undefined" class="title">
        <v-card-actions @click="onOpenSignalsSetting" style="cursor: pointer;">
          <span id="sub_title">{{$t("signal") + ' ' + $t('setting')}}</span>
          <v-spacer></v-spacer>
          <v-btn icon fab small style="width: 20px; height: 20px; margin: 0px;">
            <v-icon size="20">{{show_signals ? 'arrow_drop_up' : 'arrow_drop_down'}}</v-icon>
          </v-btn>
        </v-card-actions>
        <hr />
      </div>
      <transition name="fade">
        <v-card-text v-if="show_signals">
          <v-text-field
            :label="$t('signals')"
            :placeholder="$t('detailsetting.setsignals')"
            @input="onChangeProperty($event, 'v-text-field')"
            v-model="ui_signals"
            dense
            outlined
            hide-details
            type="text"
            style="margin-bottom: 10px;"
          ></v-text-field>
        </v-card-text>
      </transition>
      -->

      <div v-if="task_url !== null && task_url.length >= 1" class="title">
        <v-card-actions
          @click="onOpenInformationSetting"
          style="cursor: pointer;"
        >
          <span id="sub_title">{{ $t("information") }}</span>
          <v-spacer></v-spacer>
          <v-btn
            :style="this.$buttonColor()"
            icon
            fab
            small
            style="width: 20px; height: 20px; margin: 0px;"
          >
            <v-icon size="20">{{
              show_information ? "arrow_drop_up" : "arrow_drop_down"
            }}</v-icon>
          </v-btn>
        </v-card-actions>
        <hr />
      </div>
      <transition name="fade">
        <v-card-text v-if="show_information">
          <v-text-field
            :label="$t('task_url')"
            v-model="task_url"
            dense
            outlined
            hide-details
            type="text"
            style="margin-bottom: 10px;"
          ></v-text-field>
        </v-card-text>
      </transition>

      <div v-if="ui_flags.length != 0 || ui_shapes.length != 0" class="title">
        <v-card-actions @click="onOpenShapesSetting" style="cursor: pointer;">
          <span id="sub_title">{{ $t("shape") + " " + $t("setting") }}</span>
          <v-spacer></v-spacer>
          <v-btn
            :style="this.$buttonColor()"
            icon
            fab
            small
            style="width: 20px; height: 20px; margin: 0px;"
          >
            <v-icon size="20">{{
              show_flags ? "arrow_drop_up" : "arrow_drop_down"
            }}</v-icon>
          </v-btn>
        </v-card-actions>
        <hr />
      </div>
      <transition name="fade">
        <v-card-text v-if="show_flags">
          <v-btn
            :style="this.$buttonColor()"
            class="apply-btn optimize-btn"
            @click="onOptimization"
            >{{ $t("optimization_size") }}</v-btn
          >
          <div v-if="ui_shapes">
            <v-select
              v-model="ui_selected_shape"
              hide-details
              style="margin-bottom: 10px;"
              dense
              outlined
              :items="ui_shapes"
              :label="$t('shape')"
              @change="onChangeProperty($event)"
            ></v-select>
          </div>
          <template v-for="(flag, index) in ui_flags">
            <v-checkbox
              v-model="flag.value"
              :key="index"
              :label="$t(flag.key + '_style')"
              class="checkbox"
              @change="onChangeProperty($event)"
              >{{ flag.value }}</v-checkbox
            >
          </template>
        </v-card-text>
      </transition>
    </v-card-text>

    <!-- 삭제 버튼 -->
    <template v-if="isTask">
      <!--v-footer absolute height="68"-->
      <v-footer absolute height="100">
        <v-btn
          :style="this.$buttonColor()"
          small
          class="apply-btn"
          color="#424242"
        >
          {{ state }}
        </v-btn>
        <v-btn
          :style="this.$buttonColor()"
          v-if="isDatas"
          small
          class="half-btn-left"
          color="#424242"
          :disabled="!isDatas"
          @click="onSaveTask"
          >{{ $t("start") }}</v-btn
        >
        <v-btn
          :style="this.$buttonColor()"
          v-if="isDatas"
          small
          class="half-btn-right"
          color="#424242"
          :disabled="!isDatas"
          @click="onStop"
          >{{ $t("stop") }}</v-btn
        >
        <v-btn
          :style="this.$buttonColor()"
          v-if="isDatas"
          small
          class="apply-btn"
          color="error"
          :disabled="!isDatas"
          @click="onDelete"
          >{{ $t("delete") }}</v-btn
        >
        <div style="display:none;" v-for="(task, index) in tasks" :key="index">
          {{ task.state }}
        </div>
      </v-footer>
    </template>
    <template v-if="!isTask">
      <v-footer absolute height="40">
        <v-btn
          :style="this.$buttonColor()"
          v-if="isDatas"
          small
          class="apply-btn"
          color="error"
          :disabled="!isDatas"
          @click="onDelete"
          >{{ $t("delete") }}</v-btn
        >
      </v-footer>
    </template>
    <area-setting-dialog
      :dialog="vod_dialog"
      :lambda_id="id"
      :presave_data="area_data"
      :prop_name="select_prop_name"
      @onCancel="vod_dialog = $event"
      @onOk="vod_dialog = !$event"
      ref="event_area"
    ></area-setting-dialog>

    <check-dialog
      :open="checkDialog"
      :title="$t(checkDialogTitle)"
      :messages="checkMessgaes"
      :msgI18n="true"
      @onCancel="onCheckCancel"
      @onOk="onCheckOk"
    ></check-dialog>

    <v-dialog v-model="showWidget" fullscreen transition="dialog-transition">
      <div
        v-if="showWidget"
        style="position: absolute; top: 10%; left: 10%; width: 80%; height: 80%; min-width: 450px;"
      >
        <div
          v-if="metaComponent.name === 'rois_control'"
          style="width: 100%; height: 100%;"
        >
          <rois-widget
            :lambdaProps="self.ui_setting"
            :taskName="taskOfLambda"
            :lambdaUid="lambdaNtask.uid || null"
            :propertyName="propertyName"
            :metaData="metaData"
            isDialog
            @close="showWidget = false"
            @writeSuccess="writeSuccess($event, propertyName)"
          ></rois-widget>
        </div>
        <div v-else style="width: 100%; height: 100%;">
          <lambda-widget
            :lambdaProps="self.ui_setting"
            :taskName="taskOfLambda"
            :lambdaUid="lambdaNtask.uid || null"
            :propertyName="propertyName"
            :metaData="metaData"
            isDialog
            @close="showWidget = false"
            @writeSuccess="writeSuccess($event, propertyName)"
          ></lambda-widget>
        </div>
      </div>
    </v-dialog>
  </v-card>
</template>

<script>
import AreaSettingDialog from "@/components/Dialog/adlgAreaSetting.vue";
import CheckDialog from "@/components/Dialog/adlgCheck.vue";
import aColorPicker from "@/components/Picker/ColorPicker.vue";
import vJupyterSelect from "@/components/Combobox/acbJupyterSelect.vue";
import { Observable } from "rxjs";

import lambdaInfoViewer from "@/components/VisualGraph/vgLambdaInfo.vue";

import LambdaWidget from "@/components/LambdaWidget/Widget.vue";
import RoisWidget from "@/components/Graph/RoisWidget.vue";

export default {
  name: "vgDetailSetting",
  props: {},

  components: {
    AreaSettingDialog,
    CheckDialog,
    aColorPicker,
    vJupyterSelect,
    lambdaInfoViewer,
    LambdaWidget,
    RoisWidget,
  },

  data() {
    return {
      showInformation: false,

      lambdaNtask: null,
      title: "",
      type: "",
      editTitle: false,
      id: null,
      uid: "",
      taskOfLambda: "",

      propertyName: "",
      showWidget: false,
      metaData: null,
      metaComponent: null,

      ui_setting: null,
      show_properties: true,
      show_details: false,

      advance: false,

      ui_flags: [],
      show_flags: false,

      task_url: "",
      show_information: false,

      ui_signals: "",
      show_signals: false,

      ui_shapes: [],
      ui_selected_shape: null,

      area_data: null,
      select_prop_name: null,
      vod_dialog: false,

      checkDialog: false,
      checkDialogTitle: "warning",
      checkMessgaes: ["info_delete_save_value", "q_want_delete_lambdas"],

      dynamicInputSlot: false,
      inputs: [],
      show_inputs: false,
      dynamicOutputSlot: false,
      outputs: [],
      show_outputs: false,

      debounceInput: null,
      expansionInputPanel: null,
      expansionOutputPanel: null,

      tasks: null,
      statusTimer: null,
      statusSignal: false,
      state: "done",

      saveSignal: false,
      stopSignal: false,

      allData: null,

      rules: ["read_and_write", "initialize_only", "read_only"],

      selfOverview: null,

      alert_msg: null,
      alert_colors: {
        error: "rgb(231, 116, 112)",
        warn: "#ffde03",
        default: null,
      },
    };
  },

  computed: {
    // Check Ui setting - Existed data : Enabled button. Not Existed data: Disabled button.
    isDatas() {
      if (this.ui_setting) {
        return true;
      } else {
        return false;
      }
    },

    isTask() {
      if (this.type === "task") {
        return true;
      } else {
        return false;
      }
    },
  },

  watch: {
    expansionInputPanel() {
      if (
        this.expansionInputPanel !== null &&
        this.expansionInputPanel !== undefined
      ) {
        this.$nextTick().then(() => {
          setTimeout(() => {
            if (this.$refs.inputSlotText[this.expansionInputPanel]) {
              this.$refs.inputSlotText[this.expansionInputPanel].focus();
            }
          }, 100);
        });
      }
    },
    expansionOutputPanel() {
      if (
        this.expansionOutputPanel !== null &&
        this.expansionOutputPanel !== undefined
      ) {
        this.$nextTick().then(() => {
          setTimeout(() => {
            if (this.$refs.outputSlotText[this.expansionOutputPanel]) {
              this.$refs.outputSlotText[this.expansionOutputPanel].focus();
            }
          }, 100);
        });
      }
    },
  },

  methods: {
    /**
     * Initialize This page.
     * @public
     * @param {null}
     */
    initialize: function() {
      this.$debug(this.$options.name, "initialize", "start...");
      this.lambdaNtask = null;
      this.taskOfLambda = "";
      this.title = "";
      this.type = "";
      this.editTitle = false;
      this.id = null;
      this.uid = "";
      this.ui_setting = null;
      this.show_properties = true;
      this.show_details = false;
      this.propertyName = "";
      this.showWidget = false;
      this.metaData = null;
      this.metaComponent = null;
      this.ui_flags.length = 0;
      this.show_flags = false;
      this.task_url = "";
      this.show_information = false;
      this.ui_signals = "";
      this.show_signals = false;
      this.ui_shapes.length = 0;
      this.ui_selected_shape = null;
      this.area_data = null;
      this.select_prop_name = null;
      this.vod_dialog = false;
      this.checkDialog = false;
      this.checkDialogTitle = "warning";
      this.checkMessgaes = ["info_delete_save_value", "q_want_delete_lambdas"];
      this.dynamicInputSlot = false;
      this.inputs.length = 0;
      this.show_inputs = false;
      this.dynamicOutputSlot = false;
      this.outputs.length = 0;
      this.show_outputs = false;
      this.state = "Done";

      this.debounceInput = null;
      this.expansionInputPanel = null;
      this.expansionOutputPanel = null;

      this.statusSignal = false;
      this.advance = false;

      this.self = null;
      this.$debug(this.$options.name, "initialize", "done.");
    },

    alertMsg: function(alertColor, alertMsg, alertTimeout) {
      this.alert_color = alertColor;
      this.alert_msg = alertMsg;
      if (alertTimeout !== 0) {
        this.alert_timeout = alertTimeout || 5000; // default 5 second.
      } else {
        this.alert_timeout = 0; // unlimited.  please this.alert = false --> close.
      }
      this.$nextTick(() => {
        this.alert = true;
      });
    },

    /**
     * Set Flag properties.
     * @public
     * @param {flags} - flag properties data.
     */
    setFlags: function(flags) {
      if (flags) {
        if (typeof flags == "object") {
          for (var key in flags) {
            this.ui_flags.push({ key: key, value: flags[key] });
          }
        }
      }
    },

    /**
     * Load Lambda Data or Task Data.
     * @public
     * @param {LnT} - Lambda Data or Task Data.
     */
    loadData: function(LnT) {
      //step1 all intialize.
      this.initialize();
      //step 2 setData.
      this.$nextTick(() => {
        // for initailize complete.
        this.setData(LnT);
      }, 500);

      this.getGraphStatus();
    },

    setAllData: function(allData) {
      this.allData = allData;
    },

    /**
     * Setting Data.
     * @public
     * @param {LnT} - Lambda or Task
     */
    setData: function(LnT) {
      //step1 Required Settings.
      this.lambdaNtask = LnT;
      if (this.lambdaNtask.info) {
        if (this.lambdaNtask.info.meta) {
          this.metaData = this.lambdaNtask.info.meta;
        }
      }
      this.id = LnT.id;

      if (LnT.uid != null) {
        this.uid = LnT.uid;
      }

      this.type = LnT.type;
      if (this.type !== "task") {
        if (this.lambdaNtask.getJoinedTaskName) {
          this.taskOfLambda = this.lambdaNtask.getJoinedTaskName(
            this.lambdaNtask.task_id
          );
        }
      } else {
        this.task_url =
          "ipc://${STORAGE_TEMP}/CENTRAL::GRAPH::" +
          this.$store.getters["project/getSelectProject"] +
          "::" +
          LnT.title +
          ".pipe";
      }
      this.title = LnT.title;
      if (LnT.signals) {
        this.ui_signals = LnT.signals.join(",");
      } else {
        this.ui_signals = "";
      }

      //step2 Settings to each property.
      if (LnT.properties) {
        this.ui_setting = this.$util.cloneObject(LnT.properties);

        for (var index = 0; index < this.ui_setting.length; ++index) {
          this.ui_setting[index].component = this.makeComponent(
            this.ui_setting[index]
          );
        }

        //step2-1 Sort properties.
        var arrays = Object.values(this.ui_setting);
        arrays.sort(function(a, b) {
          var x = a.component.name.toLowerCase();
          var y = b.component.name.toLowerCase();
          return x > y ? -1 : x < y ? 1 : 0;
        });
        this.ui_setting = arrays;

        // detail Properties check
        for (var index = 0; index < this.ui_setting.length; index++) {
          if (this.ui_setting[index].valid.advance != null) {
            this.advance = true;
            break;
          }
        }
      }

      if (this.metaData) {
        if (Object.keys(this.metaData).length > 0) {
          this.makeMetaComponent();
        }
      }

      if (LnT.dynamicInputSlot) {
        this.dynamicInputSlot = LnT.dynamicInputSlot;
      }
      if (LnT.inputs) {
        this.inputs = this.$util.cloneObject(LnT.inputs);
      }

      if (LnT.dynamicOutputSlot) {
        this.dynamicOutputSlot = LnT.dynamicOutputSlot;
      }

      if (LnT.outputs) {
        this.outputs = this.$util.cloneObject(LnT.outputs);
      }

      //step4 Setting flags, Task have no edge.
      if (LnT.flags) {
        this.setFlags(LnT.flags);
      }

      if (LnT.shapes) {
        this.ui_shapes = this.$util.cloneObject(LnT.shapes);
        if (LnT.shape) {
          this.ui_selected_shape = this.ui_shapes[LnT.shape];
        } else {
          this.ui_selected_shape = this.ui_shapes[0];
        }
      }
      this.self = this;
      this.$debug(
        this.$options.name,
        "setData",
        "Done. DetailSetting Informations:",
        this
      );
    },

    /**
     * Make component for each property
     * @public
     * @param {ui_props} - Lambda or Task of properties.
     */
    makeComponent: function(ui_props) {
      var props = this.$util.cloneObject(ui_props);
      var component = {};
      if (props.title) {
        if (typeof props.title === "object") {
          component.label =
            props.title[this.$store.getters["language/getLanguage"]];
        } else if (typeof props.title === "string") {
          component.label = props.title;
        } else {
          component.label = props.name;
        }
      } else {
        component.label = props.name;
      }
      component.value = this.setPropertyValue(props);
      //options is component`s options
      component.valid = {};
      if (props.type.includes("roi_json")) {
        component.name = "v-btn";
        //when shown page, create button click event.
        this.$nextTick(() => {
          var line_setting = document.getElementById(props.name);
          line_setting.addEventListener("click", () => {
            this.openRoiSetting(component.value, component.label);
          });
        });
      } else {
        //Generate components by type.
        var findType = props.type;
        if (findType === "str") {
          component.name = "v-text-field";
          component.type = "text";
          if (props.valid && typeof props.valid === "object") {
            // eslint-disable-next-line no-prototype-builtins
            if (props.valid.hasOwnProperty("list")) {
              component.name = "v-select";
              if (typeof props.valid.list === "string") {
                if (props.valid.list.includes(";")) {
                  var sep = props.valid.list.split(";");
                  for (var index = 0; index < sep.length; ++index) {
                    if (sep[index] === "null") {
                      sep[index] = this.$t("null");
                    }
                  }
                  component.valid.items = sep;
                } else {
                  component.valid.items = [props.valid.list];
                }
                // eslint-disable-next-line valid-typeof
              } else if (typeof props.valid.list === "array") {
                component.valid.items = props.valid.list || [];
              } else if (typeof props.valid.list === "object") {
                component.valid.items = props.valid.list || [];
              } else {
                this.$warn(
                  this.$options.name,
                  "makeComponent",
                  "[STR type] TypeError: props valid list type:",
                  typeof props.valid.list
                );
              }
              // eslint-disable-next-line no-prototype-builtins
            } else if (props.valid.hasOwnProperty("dynamic_hint")) {
              component.name = "v-jupyter-select";
            } else if (props.valid.hasOwnProperty("password")) {
              if (props.valid.password) {
                component.type = "password";
              }
            }
          }
          // } else if (findType === "csv") {
          //   component.name = "a-csv-input";
          // type 이 label 인 lambda 가 없음.
          // hint list 원복
        } else if (findType === "label" || findType === "csv") {
          // csv 에서 사용하는 chip 타입 사용 x
          // component.name = "v-csv-field";
          component.name = "v-text-field";
          if (props.valid && typeof props.valid === "object") {
            // eslint-disable-next-line no-prototype-builtins
            if (props.valid.hasOwnProperty("hint")) {
              if (typeof props.valid.hint === "string") {
                if (props.valid.hint.includes(";")) {
                  var sep = props.valid.hint.split(";");
                  component.valid.items = sep;
                } else {
                  var tmp = [];
                  tmp.push(props.valid.hint);
                  component.valid.items = tmp;
                }
              } else if (typeof props.valid.hint === "array") {
                component.valid.items = props.valid.hint || [];
              } else {
                this.$warn(
                  this.$options.name,
                  "makeComponent",
                  "[CSV type] TypeError: props valid hint type:",
                  typeof props.valid.hint
                );
              }
            }
          }
        } else if (
          findType === "int" ||
          findType === "float" ||
          findType === "double"
        ) {
          component.name = "v-text-field";
          component.type = "number";
          component.valid.step = "any";
          if (props.valid && typeof props.valid === "object") {
            // min, max, step
            for (var key in props.valid) {
              component.valid[key] = props.valid[key];
            }
          }
        } else if (findType === "color") {
          component.name = "a-color-picker";
          component.type = "color";
          component.class = "color-picker";
          if (props.valid && typeof props.valid === "object") {
            if (props.valid.hasOwnProperty("rgb")) {
              component.valid.rgb = props.valid.rgb;
            }
          }
        } else if (findType === "bool") {
          component.name = "v-checkbox";
          component.class = "checkbox";
        } else {
          component.name = "v-text-field";
          component.type = "text";
          if (props.valid && typeof props.valid === "object") {
            // min, max, step
            for (var key in props.valid) {
              component.valid[key] = props.valid[key];
            }
          }
        }
      }
      return component;
    },

    makeMetaComponent: function() {
      var component = {};
      component.name = this.metaData.gui.name;
      this.metaComponent = component;
    },

    /**
     * Setting the value for each property.
     * @public
     * @param {ui_props} - Lambda or Task of properties.
     */
    setPropertyValue: function(ui_props) {
      var props = this.$util.cloneObject(ui_props);
      var value = null;
      // step1 is boolean?
      if (props.type === "bool") {
        if (props.value !== null && props.value !== undefined) {
          if (typeof props.value === "string") {
            props.value = props.value.toLowerCase();
            if (
              props.value === "" ||
              props.value === "0" ||
              props.value === "false"
            ) {
              value = false;
            } else if (props.value === "1" || props.value === "true") {
              value = true;
            } else {
              value = false;
              this.$warn(
                this.$options.name,
                "setPropertyValue",
                "Property value is wrong.",
                props.name,
                props.value
              );
            }
          } else if (typeof props.value === "number") {
            if (props.value <= 0) {
              value = false;
            } else {
              value = true;
            }
          } else if (typeof props.value === "boolean") {
            value = props.value;
          } else {
            if (props.value) {
              value = true;
            } else {
              value = false;
            }
          }
        } else {
          if (
            props.default_value !== null &&
            props.default_value !== undefined
          ) {
            if (typeof props.default_value === "string") {
              props.default_value = props.default_value.toLowerCase();
              if (
                props.default_value === "" ||
                props.default_value === "0" ||
                props.default_value === "false"
              ) {
                value = false;
              } else if (
                props.default_value === "1" ||
                props.default_value === "true"
              ) {
                value = true;
              } else {
                value = false;
                this.$warn(
                  this.$options.name,
                  "setPropertyValue",
                  "Property default is wrong.",
                  props.name,
                  props.default_value
                );
              }
            } else if (typeof props.default_value === "number") {
              if (props.default_value <= 0) {
                value = false;
              } else {
                value = true;
              }
            } else if (typeof props.default_value === "boolean") {
              value = props.default_value;
            } else {
              if (props.default_value) {
                value = true;
              } else {
                value = false;
              }
            }
          } else {
            value = false;
          }
        }
      } else {
        //step1 Check the property`s value
        if (
          props.value !== null &&
          props.value !== undefined &&
          !!props.value
        ) {
          value = props.value;
          //step2 Check the property`s default value
        } else if (
          props.default_value !== null &&
          props.default_value !== undefined &&
          !!props.default_value
        ) {
          value = props.default_value;
          //step3 Make default value when both value and default do not exist.
        } else {
          var temp_default = null;
          if (props.type === "str") {
            temp_default = "";
          } else if (props.type === "csv") {
            temp_default = "";
          } else if (props.type === "label") {
            temp_default = [];
          } else if (props.type === "int" || props.type === "float") {
            temp_default = 0;
          } else if (props.type.includes("roi_json")) {
            temp_default = {};
          } else {
            temp_default = "";
          }
          value = temp_default;
        }
      }
      return value;
    },

    /**
     * Check property rules.
     * @public
     * @param {string} - rule value.
     * @returns {boolean} - Show value.
     */
    checkRule: function(rule) {
      var find = this.rules.indexOf(rule);
      if (find < 0) {
        return false;
      } else {
        return true;
      }
    },

    /**
     * Check readonly rules.
     * @public
     * @param {string} - rule value.
     * @returns {boolean} - readonly value.
     */
    ruleIsReadonly: function(rule) {
      if (rule === "read_and_write") {
        return false;
      } else if (rule === "initialize_only") {
        return false;
      } else {
        return true;
      }
    },

    /**
     * Get Help(title of html attribute) text.
     * @public
     * @param {object} - help of lambda.
     */
    getHelp: function(help) {
      if (!help) {
        return this.$t("unknown");
      }
      if (help[this.$store.getters["language/getLanguage"]]) {
        return help[this.$store.getters["language/getLanguage"]];
      } else {
        return this.$t("unknown");
      }
    },

    /**
     * check And set Slots data.
     * @public
     * @param {checkSlots, dynamicType} - checkSltos: will checked slots(inputs, outputs), dynamicType: slots type.
     */
    checkSlots: function(checkSlots, dynamicType) {
      var slots = this.$util.cloneObject(checkSlots);
      var result = [];
      //step1 no empty name.
      for (var index = 0; index < slots.length; ++index) {
        // if (slots[index].name !== "" && slots[index].name !== null && slots[index].name !== undefined) {
        if (slots[index].name !== null && slots[index].name !== undefined) {
          result.push(slots[index]);
        }
      }
      //step2 catch same name.
      var names = [];
      for (var index = 0; index < result.length; ++index) {
        names.push(result[index].name);
      }
      for (var index = 0; index < names.length; ++index) {
        for (var i = index + 1; i < names.length; ++i) {
          if (names[index] === names[i]) {
            return false;
          }
        }
      }
      //step3-1 check dynamic type
      if (!dynamicType) {
        //step3-2 check empty.
        if (result.length === 0) {
          return false;
        }
      }
      return result;
    },

    /**
     * Appling the modifications to lambda or task.
     * @public
     * @param {null}
     */
    saveData: function() {
      var result = {};
      var isSuccess = true;
      var message = [this.$t("detailsetting.save_success")];
      result.title = this.title;
      result.type = this.type;
      result.id = this.id;
      result.uid = this.uid;
      if (this.ui_setting) {
        result.ui_setting = this.ui_setting;
      }
      if (this.ui_flags) {
        result.flags = this.ui_flags;
      }
      if (this.ui_signals) {
        result.signals = this.ui_signals
          .split(",")
          .map((s) => s.trim())
          .filter((s) => s.length >= 1);
      } else {
        result.signals = [];
      }
      if (this.ui_selected_shape) {
        result.shape = this.ui_selected_shape;
      }
      if (this.inputs.length > 0) {
        var checkInputs = this.checkSlots(this.inputs, this.dynamicInputSlot);
        if (checkInputs) {
          this.inputs = checkInputs;
          result.inputs = this.$util.cloneObject(this.inputs);
        } else {
          isSuccess = false;
          message = [
            this.$t("detailsetting.save_failed"),
            this.$t("detailsetting.wrong_input_slot_setting"),
          ];
        }
      }
      if (this.outputs.length > 0) {
        var checkOutputs = this.checkSlots(
          this.outputs,
          this.dynamicOutputSlot
        );
        if (checkOutputs) {
          this.outputs = checkOutputs;
          result.outputs = this.$util.cloneObject(this.outputs);
        } else {
          if (isSuccess) {
            isSuccess = false;
            message = [
              this.$t("detailsetting.save_failed"),
              this.$t("detailsetting.wrong_output_slot_setting"),
            ];
          } else {
            message.push(this.$t("detailsetting.wrong_output_slot_setting"));
          }
        }
      }

      this.$debug(this.$options.name, "saveData", "Done. Emit Data:", {
        success: isSuccess,
        msg: message,
        result: result,
      });
      /**
       * Events that occur when component`s properties save.
       * @type {Emit}
       * @param {object} - Success status, Success message, Result is will save data.
       */
      this.$emit("saveSetting", {
        success: isSuccess,
        msg: message,
        result: result,
      });
    },

    /**
     * Open Area Setting Dialog.
     * @public
     * @param {value, name} - value: area data, name: select property name.
     */
    openRoiSetting: function(value, name) {
      this.area_data = value;
      this.select_prop_name = name;
      this.vod_dialog = !this.vod_dialog;
    },

    /**
     * Make Lambda or Task Delete Event.
     * @public
     * @param {null}
     */
    deleteLambdaNTask: function() {
      /**
       * Events that occur when delete lambda or task.
       * @type {Emit}
       * @param {object} - Lambda or Task Info data.
       */
      this.$emit("deleteLambdaNTask", this.lambdaNtask);
    },

    removeGroupsItem: function(target, item) {
      target.splice(target.indexOf(item), 1);
      target = [...target];
    },

    onChangeProperty: function($event, component) {
      if (component === "v-text-field") {
        if (this.debounceInput) {
          clearTimeout(this.debounceInput);
          this.debounceInput = null;
        }
        this.debounceInput = setTimeout(() => {
          this.saveData();
        }, 400);
      } else {
        this.saveData();
      }
    },

    /**
     * Add Input Slot in Dynamic Input Slot.
     * @public
     * @param {null}
     */
    onAddInputSlot: function(mimes) {
      var name = ""; // init empty.
      var mimes = mimes || []; // init mimes;
      var type = null; // unuse.
      var link = null; // Init Unlink Status.
      var template = {
        name: name,
        mimes: mimes,
        readonly: false,
        type: type,
        link: link,
      };
      this.$debug(this.$options.name, "onAddInputSlot", "template:", template);
      this.inputs.push(template);
      this.expansionInputPanel = this.inputs.length - 1;
    },

    /**
     * Add output Slot in Dynamic Output Slot.
     * @public
     * @param {null}
     */
    onAddOutputSlot: function(mimes) {
      var name = ""; // init empty.
      var mimes = mimes || [];
      var type = null; // unuse.
      var links = null; // Init Unlink Status.
      var template = {
        name: name,
        mimes: mimes,
        readonly: false,
        type: type,
        links: links,
      };
      this.$debug(this.$options.name, "onAddOutputSlot", "template:", template);
      this.outputs.push(template);
      this.expansionOutputPanel = this.outputs.length - 1;
    },

    /**
     * Can change the title.
     * @public
     * @param {null}
     */
    onEditTitle: function() {
      this.editTitle = true;
      this.$nextTick(() => {
        if (this.$refs.title) {
          this.$refs.title.focus();
          this.$refs.title.addEventListener("focusout", () => {
            this.editTitle = false;
          });
        } else {
          this.$warn(
            this.$options.name,
            "onEditTitle",
            "Wrong upload UI. try refresh this page."
          );
        }
      });
    },

    onSaveTask: function() {
      this.$emit("onSaveTask", this.id);
    },

    onStop: function() {
      this.stopSignal = true;
    },

    /**
     * Open Deleting Check Dialog.
     * @public
     * @param {null}
     */
    onDelete: function() {
      if (this.type === "task") {
        this.checkMessgaes = [
          "info_delete_lambda_save_value",
          "q_want_delete_task",
        ];
      } else {
        this.checkMessgaes = [
          "info_delete_save_value",
          "q_want_delete_lambdas",
        ];
      }
      this.checkDialog = true;
    },

    /**
     * Stop Delete Event and Close Check Dialog.
     * @public
     * @param {null}
     */
    onCheckCancel: function() {
      this.checkDialog = false;
    },

    /**
     * Continue Delete Event.
     * @public
     * @param {null}
     */
    onCheckOk: function() {
      this.deleteLambdaNTask();
      this.checkDialog = false;
    },

    /**
     * Delete Input Slot item.
     * @public
     * @param {index} - Selected input slot index.
     */
    onDeleteInputSlot: function(index) {
      this.lambdaNtask.removeInput(index);
      this.inputs.splice(index, 1);
    },

    /**
     * Delete Output Slot item.
     * @public
     * @param {index} - Selected output slot index.
     */
    onDeleteOutputSlot: function(index) {
      this.lambdaNtask.removeOutput(index);
      this.outputs.splice(index, 1);
    },
    onOpenPropertiesSetting: function(event) {
      this.show_properties = !this.show_properties;
      if (this.show_properties) {
        this.show_inputs = false;
        this.show_details = false;
        this.show_outputs = false;
        this.show_flags = false;
        this.show_signals = false;
        this.show_information = false;
      }
    },
    onOpenDetailSetting: function(event) {
      this.show_details = !this.show_details;
      if (this.show_details) {
        this.show_properties = false;
        this.show_inputs = false;
        this.show_outputs = false;
        this.show_flags = false;
        this.show_signals = false;
        this.show_information = false;
      }
    },
    onOpenInputSlotSetting: function(event) {
      this.show_inputs = !this.show_inputs;
      if (this.show_inputs) {
        this.show_properties = false;
        this.show_details = false;
        this.show_outputs = false;
        this.show_flags = false;
        this.show_signals = false;
        this.show_information = false;
        if (this.inputs.length > 0) {
          for (var index = 0; index < this.inputs.length; ++index) {
            var inputslot = this.inputs[index];
            if (
              inputslot.name === "" ||
              inputslot.name === null ||
              inputslot.name === undefined
            ) {
              this.expansionInputPanel = index;
              return;
            }
          }
          this.expansionInputPanel = 0; // default select first item.
        }
      } else {
        this.expansionInputPanel = null;
      }
      this.expansionOutputPanel = null;
    },
    onOpenOutputSlotSetting: function(event) {
      this.show_outputs = !this.show_outputs;
      if (this.show_outputs) {
        this.show_properties = false;
        this.show_details = false;
        this.show_inputs = false;
        this.show_flags = false;
        this.show_signals = false;
        this.show_information = false;
        if (this.outputs.length > 0) {
          for (var index = 0; index < this.outputs.length; ++index) {
            var outputslot = this.outputs[index];
            if (
              outputslot.name === "" ||
              outputslot.name === null ||
              outputslot.name === undefined
            ) {
              this.expansionOutputPanel = index;
              return;
            }
          }
          this.expansionOutputPanel = 0; // default select first item.
        }
      } else {
        this.expansionOutputPanel = null;
      }
      this.expansionInputPanel = null;
    },
    onOpenSignalsSetting: function(event) {
      this.show_signals = !this.show_signals;
      if (this.show_signals) {
        this.show_properties = false;
        this.show_inputs = false;
        this.show_outputs = false;
        this.show_flags = false;
        this.show_information = false;
      }
    },
    onOpenInformationSetting: function(event) {
      this.show_information = !this.show_information;
      if (this.show_information) {
        this.show_properties = false;
        this.show_details = false;
        this.show_inputs = false;
        this.show_outputs = false;
        this.show_flags = false;
        this.show_signals = false;
      }
    },
    onOpenShapesSetting: function(event) {
      this.show_flags = !this.show_flags;
      if (this.show_flags) {
        this.show_properties = false;
        this.show_details = false;
        this.show_inputs = false;
        this.show_outputs = false;
        this.show_signals = false;
        this.show_information = false;
      }
    },
    onOptimization: function(e) {
      this.lambdaNtask.size = this.lambdaNtask.computeSize();
      this.saveData();
    },
    showPropertyWidget: function() {
      this.showWidget = true;
    },
    writeSuccess: function($data, propertyName) {
      for (var i = 0; i < this.ui_setting.length; ++i) {
        if (this.ui_setting[i].name === propertyName) {
          this.ui_setting[i].component.value = $data;
        }
      }
    },

    // GraphStatus
    getGraphStatus: function() {
      this.statusSignal = true;
      this.statusTimer = setInterval(() => {
        if (!this.statusSignal) {
          this.statusSignal = true;
          // this.setData(LnT);
        }
      }, 3000);
    },

    clearStatusTimer: function() {
      if (this.statusTimer) {
        clearInterval(this.statusTimer);
        this.statusTimer = null;
      }
    },
  },
  created() {
    /** etmpy */
  },
  mounted() {
    /** empty */
  },
  beforeDestroy() {
    if (this.debounceInput) {
      clearTimeout(this.debounceInput);
      this.debounceInput = null;
    }
  },
  subscriptions() {
    const $saveSignal = this.$watchAsObservable("saveSignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((saveSignal) => saveSignal == true);
    const $stopSignal = this.$watchAsObservable("stopSignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((stopSignal) => stopSignal == true);

    const $statusSignal = this.$watchAsObservable("statusSignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((statusSignal) => statusSignal == true);
    return {
      stopResult: Observable.combineLatest($stopSignal, (stopSignal) => ({
        stopSignal,
      })).flatMap(({ stopSignal }) =>
        this.$api
          .stopTask(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["project/getSelectProject"],
            this.title
          )
          .do((res) => {
            this.$debug(this.name, "subscriptions::stopTask", "Response:", res);
            if (!this.isPlaying) {
              this.alertMsg(this.alert_colors.error, [
                this.$t("execute_failed"),
              ]);
            }
            this.stopSignal = false;
          })
          .catch((err) => {
            this.$error(this.name, "subscriptions::stopTask", err);
            this.alertMsg(this.alert_colors.error, [this.$t("execute_failed")]);
            return Observable.of(null);
          })
          .do(() => {
            this.stopSignal = false;
          })
      ),

      // 그래프 상태 확인
      statusResult: Observable.combineLatest($statusSignal, (statusSignal) => ({
        statusSignal,
        // eslint-disable-next-line no-unused-vars
      })).flatMap(({ statusSignal }) =>
        this.$api
          .getGraphStatus(
            this.$store.getters["user/getAccessToken"],
            null,
            this.$store.getters["project/getSelectProject"]
          )
          .do((res) => {
            var response = res.result.obj;
            var tasks = response.tasks;
            for (var task of tasks) {
              if (this.title == task.name) {
                this.state = task.state;
              }
            }
          })
          .catch((err) => {
            this.$error(this.name, "subscriptions::getGraphStatus", err);
            return Observable.of(null);
          })
          .do(() => {
            this.statusSignal = false;
          })
      ),
    };
  },
};
</script>

<style scoped>
hr {
  margin-bottom: 5px;
}
.v-toolbar >>> .v-toolbar__content {
  padding: 0 0 0 0;
  padding-left: 15px;
  /* padding-right: 5px; */
}
#main-detail {
  width: 100%;
  height: 100%;
  word-break: break-all;
}
#title-zone {
  position: absolute;
  width: 100%;
  top: 34px;
  padding-left: 10px;
  padding-right: 10px;
}
#title:focus {
  border: 1px solid white;
  border-radius: 4px;
  outline: none;
}
#edit-zone {
  position: absolute;
  width: 100%;
  height: calc(100% - 100px);
  top: 60px;
  padding-left: 15px;
  padding-right: 15px;
  overflow: auto;
}
#sub_title {
  font-size: 13.5px;
}
#preview_btn {
  width: 100%;
  margin: 0 0 0 0;
  border: 1px solid #bbb;
}
.title {
  width: 100%;
  padding-left: 5px;
  padding-right: 5px;
}
.edit-zone {
  position: absolute;
  width: 100%;
  height: calc(100% - 96px);
  top: 48px;
  overflow: auto;
}
.optimize-btn {
  margin-bottom: 10px !important;
}
.apply-btn {
  margin-bottom: 4px;
  width: 100%;
  border: 1px solid #bbb;
}
.half-btn-left {
  margin-right: 1%;
  margin-bottom: 4px;
  width: 49%;
  border: 1px solid #bbb;
}
.half-btn-right {
  margin-left: 1%;
  margin-bottom: 4px;
  width: 49%;
  border: 1px solid #bbb;
}
.checkbox {
  margin: 0 0 0 0;
  margin-bottom: 8px;
  padding-left: 5px;
  height: 42px;
  border: 2px solid #cbcbcb;
  border-radius: 4px;
  align-items: center;
}
.checkbox:hover {
  border: 2px solid #ffffff;
}
.color-picker {
  height: 58px;
  border: 2px solid white;
  border-radius: 4px;
  margin-bottom: 8px;
  padding-top: 5px;
  padding-bottom: 0px;
  padding-left: 5px;
  padding-right: 5px;
}

.roi_setting {
  margin-bottom: 8px;
}

/* Vuetify Style Change */
.v-footer {
  padding-left: 10px;
  padding-right: 10px;
}
.v-card__text {
  padding-left: 5px;
  padding-right: 5px;
}
.v-input >>> .v-messages {
  min-height: 0 !important;
  height: 0 !important;
  min-width: 0 !important;
  width: 0 !important;
}
.v-input >>> .v-input__slot {
  margin: 0 !important;
}
.v-input--switch {
  margin: 0;
}
.menu-title {
  height: 40px;
  display: flex;
  align-items: center;
  padding-left: 10px;
  padding-right: 10px;
}

/* Transition */
.fade-enter-active {
  transition: opacity 0s;
}
.fade-leave-active {
  transition: opacity 0s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.slide-fade-enter-active {
  transition: all 0.3s ease;
}
.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  transform: translateX(10px);
  opacity: 0;
}
.bounce-enter-active {
  animation: bounce-in 0.5s;
}
.bounce-leave-active {
  animation: bounce-in 0.3s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  30% {
    transform: scale(1.3);
  }
  100% {
    transform: scale(1);
  }
}
.close--icon {
  position: absolute;
  top: -10px;
  right: -10px;
  border: 1px solid;
  border-radius: 15px;
}
</style>
