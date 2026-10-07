param([string]$path)
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder,Windows.Foundation,ContentType=WindowsRuntime]
$null = [Windows.Storage.StorageFile,Windows.Foundation,ContentType=WindowsRuntime]
function Await($op,[Type]$t){
  $m=[System.WindowsRuntimeSystemExtensions].GetMethods()|?{$_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'}|select -First 1
  $g=$m.MakeGenericMethod($t); $task=$g.Invoke($null,@($op)); $task.Wait(-1)|Out-Null; $task.Result }
$file=Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($path)) ([Windows.Storage.StorageFile])
$stream=Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
$dec=Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
$bmp=Await ($dec.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
$eng=[Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$res=Await ($eng.RecognizeAsync($bmp)) ([Windows.Media.Ocr.OcrResult])
$res.Text
