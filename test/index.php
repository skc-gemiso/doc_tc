<?php
define('PYTHON_BIN',  'python3.12');
define('MAIN_PY',     '/app/proxima-v6/external/doc_tc/doc_tc.py');
define('INPUT_DIR',   '/app/proxima-v6/tests/input');
define('OUTPUT_DIR',  '/app/proxima-v6/tests/output');
define('CALLBACK_URL', 'http://localhost/tests/callback.php');

$message = '';
$result  = null;

// 파일 업로드 처리
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['srcFile'])) {
    $file    = $_FILES['srcFile'];
    $allowed = ['doc','docx','xls','xlsx','ppt','pptx','odt','ods','odp','txt','csv','rtf','html','pdf'];
    $ext     = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));

    if ($file['error'] !== UPLOAD_ERR_OK) {
        $message = '업로드 오류: ' . $file['error'];
    } elseif (!in_array($ext, $allowed, true)) {
        $message = '지원하지 않는 파일 형식입니다: ' . $ext;
    } else {
        @mkdir(INPUT_DIR,  0755, true);
        @mkdir(OUTPUT_DIR, 0755, true);

        $srcPath = INPUT_DIR  . '/' . basename($file['name']);
        $tarPath = OUTPUT_DIR . '/' . pathinfo($file['name'], PATHINFO_FILENAME) . '.pdf';

        if (!move_uploaded_file($file['tmp_name'], $srcPath)) {
            $message = '파일 저장 실패';
        } else {
            $task = [
                'taskId'      => (int)($_POST['taskId'] ?? 1),
                'srcPath'     => $srcPath,
                'isThumbNail' => isset($_POST['isThumbNail']),
                'isCatalog'   => isset($_POST['isCatalog']),
                'width'       => (int)($_POST['width']  ?? 700),
                'height'      => (int)($_POST['height'] ?? 500),
                'tarPath'     => $tarPath,
                'callBack'    => CALLBACK_URL,
            ];

            $json = json_encode($task, JSON_UNESCAPED_UNICODE);
            $cmd  = sprintf(
                "echo %s | %s %s 2>&1",
                escapeshellarg($json),
                escapeshellcmd(PYTHON_BIN),
                escapeshellarg(MAIN_PY)
            );

            exec($cmd, $output, $exitCode);

            $result = [
                'cmd'      => $cmd,
                'exitCode' => $exitCode,
                'output'   => implode("\n", $output),
                'task'     => $task,
            ];

            $message = $exitCode === 0 ? '변환 성공' : '변환 실패';
        }
    }
}
?>
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>문서 변환 테스트</title>
<style>
  body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }
  h1 { font-size: 1.4rem; border-bottom: 2px solid #333; padding-bottom: 8px; }
  label { display: block; margin: 12px 0 4px; font-weight: bold; }
  input[type=text], input[type=number] { width: 100%; padding: 6px; box-sizing: border-box; }
  input[type=file] { padding: 4px 0; }
  .row { display: flex; gap: 20px; }
  .row > div { flex: 1; }
  button { margin-top: 20px; padding: 10px 30px; background: #2563eb; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 1rem; }
  button:hover { background: #1d4ed8; }
  .message { margin-top: 16px; padding: 10px; border-radius: 4px; font-weight: bold; }
  .success { background: #d1fae5; color: #065f46; }
  .error   { background: #fee2e2; color: #991b1b; }
  .result  { margin-top: 20px; }
  .result h2 { font-size: 1rem; margin-bottom: 6px; }
  pre { background: #f3f4f6; padding: 12px; border-radius: 4px; overflow-x: auto; font-size: 0.85rem; white-space: pre-wrap; word-break: break-all; }
</style>
</head>
<body>
<h1>문서 변환 테스트</h1>

<form method="POST" enctype="multipart/form-data">
  <label>Task ID</label>
  <input type="number" name="taskId" value="<?= htmlspecialchars($_POST['taskId'] ?? '1') ?>">

  <label>변환할 문서 파일</label>
  <input type="file" name="srcFile" required>

  <div class="row">
    <div>
      <label>썸네일 가로 (width)</label>
      <input type="number" name="width" value="<?= htmlspecialchars($_POST['width'] ?? '700') ?>">
    </div>
    <div>
      <label>썸네일 세로 (height)</label>
      <input type="number" name="height" value="<?= htmlspecialchars($_POST['height'] ?? '500') ?>">
    </div>
  </div>

  <label>
    <input type="checkbox" name="isThumbNail" <?= isset($_POST['isThumbNail']) ? 'checked' : '' ?>>
    썸네일 생성 (isThumbNail)
  </label>

  <label>
    <input type="checkbox" name="isCatalog" <?= isset($_POST['isCatalog']) ? 'checked' : '' ?>>
    카탈로그 생성 (isCatalog)
  </label>

  <button type="submit">변환 실행</button>
</form>

<?php if ($message): ?>
<div class="message <?= $result && $result['exitCode'] === 0 ? 'success' : 'error' ?>">
  <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<?php if ($result): ?>
<div class="result">
  <h2>요청 파라미터</h2>
  <pre><?= htmlspecialchars(json_encode($result['task'], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)) ?></pre>

  <h2>실행 로그</h2>
  <pre><?= htmlspecialchars($result['output'] ?: '(출력 없음)') ?></pre>
</div>
<?php endif; ?>

</body>
</html>
