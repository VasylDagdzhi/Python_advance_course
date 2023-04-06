function updateMemoryStats() {
        fetch('/stats/virtual_memory')
          .then((response) => response.json())
          .then((data) => {
            // Calculate the RAM values in GB
            const freeMemoryInGb = data.free / 1024 / 1024 / 1024;
            const totalMemoryInGb = data.total / 1024 / 1024 / 1024;
            const availableMemoryInGb = data.available / 1024 / 1024 / 1024;
            const usedMemoryInGb = data.used / 1024 / 1024 / 1024;
            const cachedMemoryInGb = data.cached / 1024 / 1024 / 1024;
            // Calculate the percentage
            let percent = (freeMemoryInGb / totalMemoryInGb) * 100;
            // Set the labels
            pb1_leftlabel.textContent = `Free RAM: ${freeMemoryInGb.toFixed(1)} GB | ${percent.toFixed(0)}%`;
            pb1_rightlabel.textContent = `All RAM: ${totalMemoryInGb.toFixed(1)} GB`;
            // Set the progress bar pb1_fill width
            pb1_fill.style.width = `${percent.toFixed(0)}%`;
            // recalculate the percentage for the second block
            percent = (availableMemoryInGb / totalMemoryInGb) * 100;
            // Set the labels
            pb2_leftlabel.textContent = `Available RAM: ${availableMemoryInGb.toFixed(1)} GB | ${percent.toFixed(0)}%`;
            pb2_rightlabel.textContent = `All RAM: ${totalMemoryInGb.toFixed(1)} GB`;
            // Set the progress bar pb2_fill width
            pb2_fill.style.width = `${percent.toFixed(0)}%`;
            // recalculate the percentage for the third block
            percent = (usedMemoryInGb / totalMemoryInGb) * 100;
            // Set the labels
            pb3_leftlabel.textContent = `Used RAM: ${usedMemoryInGb.toFixed(1)} GB | ${percent.toFixed(0)}%`;
            pb3_rightlabel.textContent = `All RAM: ${totalMemoryInGb.toFixed(1)} GB`;
            // Set the progress bar pb3_fill width
            pb3_fill.style.width = `${percent.toFixed(0)}%`;
            // recalculate the percentage for the fourth block
            percent = (cachedMemoryInGb / totalMemoryInGb) * 100;
            // Set the labels
            pb4_leftlabel.textContent = `Cached RAM: ${cachedMemoryInGb.toFixed(1)} GB | ${percent.toFixed(0)}%`;
            pb4_rightlabel.textContent = `All RAM: ${totalMemoryInGb.toFixed(1)} GB`;

            // Set the progress bar pb4_fill width
            pb4_fill.style.width = `${percent.toFixed(0)}%`;
            // Get references to the HTML elements
            const totalElem = document.querySelector("#total");
            const freeElem = document.querySelector("#free");
            const usedElem = document.querySelector("#used");
            const cacheElem = document.querySelector("#cache");

            totalFormula.textContent = `Formula: ${((data.used / (1024 ** 3)).toFixed(2))} + ${((data.free / (1024 ** 3)).toFixed(2))} + ${((data.cached / (1024 ** 3)).toFixed(2))} + ${((data.shared / (1024 ** 3)).toFixed(2))} ~ ${((data.total / (1024 ** 3)).toFixed(2))}`;
            totalValues.textContent = `Values: ${((data.used / (1024 ** 3)) + (data.free / (1024 ** 3)) + (data.cached / (1024 ** 3)) + (data.shared / (1024 ** 3))).toFixed(2)} ~ ${((data.total / (1024 ** 3)).toFixed(2))}`;

            freeFormula.textContent = `Formula: ${((data.total / (1024 ** 3)).toFixed(2))} - ${((data.used / (1024 ** 3)).toFixed(2))} - ${((data.cached / (1024 ** 3)).toFixed(2))} - ${((data.shared / (1024 ** 3)).toFixed(2))} ~ ${((data.free / (1024 ** 3)).toFixed(2))}`;
            freeValues.textContent = `Values: ${(data.total / (1024 ** 3) - data.used / (1024 ** 3) - data.cached / (1024 ** 3) - data.shared / (1024 ** 3)).toFixed(2)} ~ ${(data.free / (1024 ** 3)).toFixed(2)}`;

            usedFormula.textContent = `Formula: ${((data.total / (1024 ** 3)).toFixed(2))} - ${((data.free / (1024 ** 3)).toFixed(2))} - ${((data.cached / (1024 ** 3)).toFixed(2))} - ${((data.shared / (1024 ** 3)).toFixed(2))} ~ ${((data.used / (1024 ** 3)).toFixed(2))}`;
            usedValues.textContent = `Values: ${((data.total / (1024 ** 3)) - (data.free / (1024 ** 3)) - (data.cached / (1024 ** 3)) - (data.shared / (1024 ** 3))).toFixed(2)} ~ ${(data.used / (1024 ** 3)).toFixed(2)}`;

            cacheFormula.textContent = `Formula: ${(data.total / (1024 ** 3)).toFixed(2)} - ${(data.free / (1024 ** 3)).toFixed(2)} - ${(data.used / (1024 ** 3)).toFixed(2)} - ${(data.shared / (1024 ** 3)).toFixed(2)} ~ ${(data.cached / (1024 ** 3)).toFixed(2)}`;
            cacheValues.textContent = `Values: ${((data.total / (1024 ** 3)) - (data.free / (1024 ** 3)) - (data.used / (1024 ** 3)) - (data.shared / (1024 ** 3))).toFixed(2)} ~ ${(data.cached / (1024 ** 3)).toFixed(2)}`;

          });
      }

updateMemoryStats();
setInterval(updateMemoryStats, 1000);