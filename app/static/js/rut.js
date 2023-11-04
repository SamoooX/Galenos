function validarRut(rut) {
      // Limpia el RUT y convierte a mayúsculas la letra verificadora
      rut = rut.replace('.', '').replace('-', '').toUpperCase();
    
      // Verifica que el RUT tenga un formato válido
      if (!/^\d{7,8}[0-9kK]{1}$/.test(rut)) {
        document.getElementById("mensajeValidacion").textContent = "RUT no válido";
        return;
      }
    
      // Divide el RUT en su parte numérica y la letra verificadora
      var rutNumerico = rut.substring(0, rut.length - 1);
      var digitoVerificador = rut.slice(-1);
    
      // Calcula el dígito verificador correcto
      var dvCalculado = dgv(parseInt(rutNumerico, 10));
    
      // Compara el dígito verificador calculado con el dígito verificador ingresado
      if (dvCalculado != digitoVerificador) {
        document.getElementById("mensajeValidacion").textContent = "RUT no válido";
        document.getElementById("botonV").disabled = true;
      }else{
        document.getElementById("mensajeValidacion").textContent = "";
        document.getElementById("botonV").disabled = false;
      }
    }
    
    function dgv(T) {
      var M=0,S=1;
      for (;T;T=Math.floor(T/10))
        S = (S + T % 10 * (9 - M++ % 6)) % 11;
      return S ? S - 1 : 'K';
    }