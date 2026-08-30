import * as hmUI from '@zos/ui'
import { Battery, Step, Time } from '@zos/sensor'
import { log } from '@zos/utils'

/* Raster 90 static Balance face.
 *
 * This uses the Zepp OS v3 module APIs intentionally: the 480px target is the
 * native Amazfit Balance canvas, while each generated image still comes from
 * the canonical Raster 90 3x3-cell matrices.  Only the IMG_TIME digits and
 * static colon are visible in AOD; all data rows are normal-mode-only.
 */

var logger = log.getLogger('raster90')
var ORIGIN_X = 15
var ORIGIN_Y = 15
var ONLY_NORMAL = hmUI.show_level.ONLY_NORMAL
var NORMAL_AND_AOD = hmUI.show_level.ONLY_NORMAL | hmUI.show_level.ONAL_AOD

var FINE_HEIGHT = 21
var ICON_SIZE = 48
var TIME_HEIGHT = 96

var timeWidget = null
var dateWidgets = []
var weatherIcon = null
var stepText = null
var batteryIcon = null
var timeSensor = null
var stepSensor = null
var batterySensor = null
var dateTimer = null
var resumeDelegate = null
var stepChangeCallback = null
var batteryChangeCallback = null

var digitAssets = [
  'images/text/0.png',
  'images/text/1.png',
  'images/text/2.png',
  'images/text/3.png',
  'images/text/4.png',
  'images/text/5.png',
  'images/text/6.png',
  'images/text/7.png',
  'images/text/8.png',
  'images/text/9.png',
]

var weatherAssets = [
  'images/weather-bound/00.png',
  'images/weather-bound/01.png',
  'images/weather-bound/02.png',
  'images/weather-bound/03.png',
  'images/weather-bound/04.png',
  'images/weather-bound/05.png',
  'images/weather-bound/06.png',
  'images/weather-bound/07.png',
  'images/weather-bound/08.png',
  'images/weather-bound/09.png',
  'images/weather-bound/10.png',
  'images/weather-bound/11.png',
  'images/weather-bound/12.png',
  'images/weather-bound/13.png',
  'images/weather-bound/14.png',
  'images/weather-bound/15.png',
  'images/weather-bound/16.png',
  'images/weather-bound/17.png',
  'images/weather-bound/18.png',
  'images/weather-bound/19.png',
  'images/weather-bound/20.png',
  'images/weather-bound/21.png',
  'images/weather-bound/22.png',
  'images/weather-bound/23.png',
  'images/weather-bound/24.png',
  'images/weather-bound/25.png',
  'images/weather-bound/26.png',
  'images/weather-bound/27.png',
  'images/weather-bound/28.png',
]

var weekdayNames = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
var monthNames = [
  'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
  'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC',
]

function image(path) {
  return 'images/' + path
}

function textImageName(character) {
  if (character === ' ') return 'space'
  if (character === '-') return 'minus'
  if (character === '%') return 'percent'
  if (character === '°') return 'degree'
  return character.toLowerCase()
}

function textImage(character) {
  return image('text/' + textImageName(character) + '.png')
}

function setSource(widget, source) {
  if (widget) widget.setProperty(hmUI.prop.SRC, source)
}

function createImage(x, y, width, height, source, showLevel) {
  return hmUI.createWidget(hmUI.widget.IMG, {
    x: x,
    y: y,
    w: width,
    h: height,
    src: source,
    show_level: showLevel,
  })
}

function createDate() {
  // SAT 15 AUG is the fixed-width preview/default.  Spaces are two source
  // cells (6px); every other compact glyph has an 18px authored advance.
  // Positions are active-frame-local; adding (15,15) yields the native
  // preview coordinates 162, 180, 198, 216, 222, 240, 258, 264, 282, 300.
  var xPositions = [147, 165, 183, 201, 207, 225, 243, 249, 267, 285]
  var widths = [18, 18, 18, 6, 18, 18, 6, 18, 18, 18]
  var initial = 'SAT 15 AUG'
  for (var i = 0; i < initial.length; i += 1) {
    dateWidgets.push(createImage(
      ORIGIN_X + xPositions[i],
      ORIGIN_Y + 111 + 13,
      widths[i],
      FINE_HEIGHT,
      textImage(initial.charAt(i)),
      ONLY_NORMAL,
    ))
  }
}

function weekdayIndex(value) {
  if (typeof value !== 'number' || value !== value) return 6
  // The documented TIME sensor is Monday=1 through Sunday=7.  Accept a
  // Sunday=0 implementation as well so the date remains truthful across OS
  // revisions.
  if (value >= 1 && value <= 7) return value % 7
  if (value >= 0 && value <= 6) return value
  return 6
}

function dateText() {
  if (!timeSensor) return 'SAT 15 AUG'
  var day = Number(timeSensor.getDate())
  var month = Number(timeSensor.getMonth())
  if (!isFinite(day) || day < 1 || day > 31 || !isFinite(month) || month < 1 || month > 12) {
    return 'SAT 15 AUG'
  }
  var dayText = day < 10 ? '0' + day : '' + day
  return weekdayNames[weekdayIndex(Number(timeSensor.getDay()))] + ' ' + dayText + ' ' + monthNames[month - 1]
}

function updateDate() {
  var value = dateText()
  for (var i = 0; i < dateWidgets.length && i < value.length; i += 1) {
    setSource(dateWidgets[i], textImage(value.charAt(i)))
  }
}

function createTime() {
  timeWidget = hmUI.createWidget(hmUI.widget.IMG_TIME, {
    hour_zero: 1,
    hour_startX: ORIGIN_X + 54,
    hour_startY: ORIGIN_Y + 177,
    hour_array: [
      image('time/0.png'),
      image('time/1.png'),
      image('time/2.png'),
      image('time/3.png'),
      image('time/4.png'),
      image('time/5.png'),
      image('time/6.png'),
      image('time/7.png'),
      image('time/8.png'),
      image('time/9.png'),
    ],
    hour_space: 0,
    minute_zero: 1,
    minute_startX: ORIGIN_X + 240,
    minute_startY: ORIGIN_Y + 177,
    minute_array: [
      image('time/0.png'),
      image('time/1.png'),
      image('time/2.png'),
      image('time/3.png'),
      image('time/4.png'),
      image('time/5.png'),
      image('time/6.png'),
      image('time/7.png'),
      image('time/8.png'),
      image('time/9.png'),
    ],
    minute_space: 0,
    show_level: NORMAL_AND_AOD,
  })
  createImage(
    ORIGIN_X + 210,
    ORIGIN_Y + 177,
    30,
    TIME_HEIGHT,
    image('time/colon.png'),
    NORMAL_AND_AOD,
  )
}

function createWeather() {
  logger.info('native weather type: ' + hmUI.data_type.WEATHER)
  createImage(
    ORIGIN_X + 162,
    ORIGIN_Y + 45,
    ICON_SIZE,
    ICON_SIZE,
    image('weather/25.png'),
    ONLY_NORMAL,
  )

  weatherIcon = hmUI.createWidget(hmUI.widget.IMG_LEVEL, {
    x: ORIGIN_X + 162,
    y: ORIGIN_Y + 45,
    w: ICON_SIZE,
    h: ICON_SIZE,
    image_array: weatherAssets,
    image_length: weatherAssets.length,
    type: hmUI.data_type.WEATHER,
    show_level: ONLY_NORMAL,
  })

  hmUI.createWidget(hmUI.widget.TEXT_IMG, {
    x: ORIGIN_X + 216,
    y: ORIGIN_Y + 45 + 13,
    w: 108,
    h: FINE_HEIGHT,
    font_array: digitAssets,
    type: hmUI.data_type.WEATHER_CURRENT,
    unit_sc: image('unit/celsius.png'),
    unit_tc: image('unit/celsius.png'),
    unit_en: image('unit/celsius.png'),
    imperial_unit_sc: image('unit/fahrenheit.png'),
    imperial_unit_tc: image('unit/fahrenheit.png'),
    imperial_unit_en: image('unit/fahrenheit.png'),
    negative_image: image('text/minus.png'),
    invalid_image: image('text/double-minus.png'),
    h_space: 0,
    align_h: hmUI.align.LEFT,
    show_level: ONLY_NORMAL,
  })
}

function createSteps() {
  createImage(
    ORIGIN_X + 153,
    ORIGIN_Y + 291,
    ICON_SIZE,
    ICON_SIZE,
    image('utility/steps.png'),
    ONLY_NORMAL,
  )
  stepText = hmUI.createWidget(hmUI.widget.TEXT_IMG, {
    x: ORIGIN_X + 207,
    y: ORIGIN_Y + 291 + 13,
    w: 90,
    h: FINE_HEIGHT,
    font_array: digitAssets,
    text: '00000',
    h_space: 0,
    align_h: hmUI.align.LEFT,
    show_level: ONLY_NORMAL,
  })
}

function formatSteps(value) {
  var current = Number(value)
  if (!isFinite(current) || current < 0) current = 0
  current = Math.min(99999, Math.floor(current))
  var result = '' + current
  while (result.length < 5) result = '0' + result
  return result
}

function updateSteps() {
  var current = 0
  try {
    if (stepSensor) current = stepSensor.getCurrent()
  } catch (error) {
    logger.warn('step refresh failed: ' + error)
  }
  if (stepText) stepText.setProperty(hmUI.prop.TEXT, formatSteps(current))
}

function batteryBand(value) {
  if (typeof value !== 'number' || value !== value) return 'white'
  if (value > 50) return 'white'
  if (value > 25) return 'yellow'
  if (value > 10) return 'orange'
  return 'red'
}

function updateBattery() {
  var current = null
  if (batterySensor) current = Number(batterySensor.getCurrent())
  setSource(batteryIcon, image('utility/battery-' + batteryBand(current) + '.png'))
}

function createBattery() {
  batteryIcon = createImage(
    ORIGIN_X + 171,
    ORIGIN_Y + 357,
    ICON_SIZE,
    ICON_SIZE,
    image('utility/battery-white.png'),
    ONLY_NORMAL,
  )
  hmUI.createWidget(hmUI.widget.TEXT_IMG, {
    x: ORIGIN_X + 225,
    y: ORIGIN_Y + 357 + 13,
    w: 72,
    h: FINE_HEIGHT,
    font_array: digitAssets,
    type: hmUI.data_type.BATTERY,
    unit_sc: image('text/percent.png'),
    unit_tc: image('text/percent.png'),
    unit_en: image('text/percent.png'),
    h_space: 0,
    align_h: hmUI.align.LEFT,
    show_level: ONLY_NORMAL,
  })
}

function createResumeDelegate() {
  resumeDelegate = hmUI.createWidget(hmUI.widget.WIDGET_DELEGATE, {
    resume_call: function () {
      updateDate()
      updateSteps()
      updateBattery()
    },
  })
}

function bindSensors() {
  try {
    timeSensor = new Time()
  } catch (error) {
    logger.warn('time sensor unavailable: ' + error)
    timeSensor = null
  }
  dateTimer = setInterval(updateDate, 60 * 1000)

  try {
    stepSensor = new Step()
    if (stepSensor && stepSensor.onChange) {
      stepChangeCallback = updateSteps
      stepSensor.onChange(stepChangeCallback)
    }
  } catch (error) {
    logger.warn('step sensor unavailable: ' + error)
    stepSensor = null
  }

  try {
    batterySensor = new Battery()
    if (batterySensor && batterySensor.onChange) {
      batteryChangeCallback = updateBattery
      batterySensor.onChange(batteryChangeCallback)
    }
  } catch (error) {
    logger.warn('battery sensor unavailable: ' + error)
    batterySensor = null
  }
}

function releaseSensors() {
  if (stepSensor && stepChangeCallback && stepSensor.offChange) {
    try {
      stepSensor.offChange(stepChangeCallback)
    } catch (error) {
      logger.warn('step listener cleanup failed: ' + error)
    }
  }
  if (batterySensor && batteryChangeCallback && batterySensor.offChange) {
    try {
      batterySensor.offChange(batteryChangeCallback)
    } catch (error) {
      logger.warn('battery listener cleanup failed: ' + error)
    }
  }
  timeSensor = null
  stepSensor = null
  batterySensor = null
  stepChangeCallback = null
  batteryChangeCallback = null
}

function buildFace() {
  logger.info('build start')
  createTime()
  logger.debug('time widget created')
  createWeather()
  logger.debug('weather widgets created')
  createDate()
  createSteps()
  createBattery()
  logger.debug('data widgets created')
  bindSensors()
  logger.debug('sensors bound')
  createResumeDelegate()
  updateDate()
  updateSteps()
  updateBattery()
  logger.info('build complete')
}

WatchFace({
  onInit() {
    logger.info('onInit')
  },

  build() {
    buildFace()
  },

  onDestroy() {
    logger.info('onDestroy')
    if (dateTimer) clearInterval(dateTimer)
    dateTimer = null
    releaseSensors()
    resumeDelegate = null
  },
})
