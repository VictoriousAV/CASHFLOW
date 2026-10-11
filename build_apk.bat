@echo off
setlocal
rem CashFlow AI - Windows build script for the release APK
rem Requires: JDK 17 (keytool/java), Android SDK with build-tools 34.0.0
set "ROOT=%~dp0"
set "JAVA_HOME=C:\Program Files\Java\jdk-17.0.1"
set "ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk"

if not exist "%ROOT%android\keystore.properties" (
  echo ERROR: android\keystore.properties not found.
  echo The release keystore must exist at android\keystore\cashflow-release.keystore.
  exit /b 1
)

echo Building signed release APK...
cd /d "%ROOT%android"
call gradlew.bat assembleRelease --no-daemon
if errorlevel 1 (
  echo BUILD FAILED - see messages above.
  exit /b 1
)

if not exist "%ROOT%dist" mkdir "%ROOT%dist"
copy /Y "%ROOT%android\app\build\outputs\apk\release\app-release.apk" "%ROOT%dist\CashFlowAI-1.0-release.apk" >nul

echo.
echo APK : %ROOT%dist\CashFlowAI-1.0-release.apk
echo SHA256:
certutil -hashfile "%ROOT%dist\CashFlowAI-1.0-release.apk" SHA256 | findstr /v /c:"hash" /c:"CertUtil"
echo Done.
exit /b 0
