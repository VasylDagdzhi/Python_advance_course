function updateMemoryStats() {
        fetch('/stats/virtual_memory')
          .then((response) => response.json())
          .then((data) => {
            let freeMemoryInGb = data.free / 1024 / 1024 / 1024;
            let totalMemoryInGb = data.total / 1024 / 1024 / 1024;
            document.querySelector('#available-memory').textContent = `Available memory: ${freeMemoryInGb.toFixed(2)} / ${totalMemoryInGb.toFixed(2)} GB | ${data.percent}%`;
            document.querySelector('.bar').style.transform = `translate(${data.percent}%)`;
            document.querySelector('.data').style.width = `${data.percent}%`;
          });
      }

updateMemoryStats();
setInterval(updateMemoryStats, 1000);