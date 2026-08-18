plugins {
    alias(libs.plugins.android.application)
}

android {
    enableKotlin = false
    namespace = "io.github.byebyebryan.raster90.watchface"
    compileSdk = 35

    defaultConfig {
        applicationId = "io.github.byebyebryan.raster90.watchface"
        minSdk = 34
        targetSdk = 35
        versionCode = 1
        versionName = "0.1.0"
    }

    buildTypes {
        debug {
            isMinifyEnabled = false
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = false
        }
    }
}
