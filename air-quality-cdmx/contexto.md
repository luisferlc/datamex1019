{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Predicción del IMECA en CDMX (PM10 y PM2.5)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Contexto/Intro"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Con base a la Norma Ambiental para el Distrito Federal NADF-009-AIRE-2017 (14 de noviembre de 2018), y la NOM-025-SSA1-2014 (20 de agosto de 2014): Criterios para evaluar la calidad del aire ambiente, con respecto a las partículas suspendidas totales, las partículas menores de 10 micrómetros y las partículas menores de 2.5 micrómetros). Las más actualizadas hasta el momento:\n",
    "\n",
    "### Consecuencias de la mala calidad del aire en general:\n",
    "- En 2012, según la OMS , al año mueren más de 7 millones de personas. Y 1 de cada 8 de esos 7 millones, se debe a por la exposición a la contaminación del aire.\n",
    "-  En 2013, la Agencia Internacional para la Investigación en Cáncer (IARC por sus siglas en inglés) designó a la contaminación atmosférica como agente cancerígeno en humanos del Grupo 1.\n",
    "\n",
    "### Consecuencias de las partículas PM10 y PM2.5\n",
    "- Reducciones agudas en el volumen espiratorio forzado del primer segundo (FEV1) y en la capacidad vital forzada (FVC). Esto se traduce a capacidad pulmonar.\n",
    "- En individuos asmáticos, aun pequeñas exposiciones a PM2.5 y PM10 se han asociado con inflamación neutrofílica y disminución del potencial de hidrógeno (pH) en las vías aéreas.\n",
    "- La exposición a largo plazo a niveles altos de PM2.5 se asocia significativamente a hospitalizaciones por neumonía adquirida, mientras que la exposición a PM10 durante los meses de verano se asocia con mayores síntomas de apnea obstructiva y menor saturación durante el sueño.\n",
    "- Cambios en la variabilidad de la frecuencia cardiaca (PM2.5).\n",
    "- Incremento en la mortalidad por causas no externas, principalmente cardiovasculares y respiratorias; también se ha relacionado con la mortalidad postneonatal.\n",
    "\n",
    "Entre otras...\n",
    "\n",
    "Actualmente, en la Ciudad de México se rebasan los límites máximos permisibles de ozono y de partículas suspendidas en varios días al año, y como consecuencia la población vulnerable es la más afectada debido al deterioro en la calidad del aire. "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Al detectar la concentración de contaminantes del aire ambiente estamos determinando su  calidad.  Así  entonces,  la  calidad  del  aire puede ser definida por indicadores o índices preestablecidos  que  determinan  la  concentración de contaminantes en el aire ambiente ligada a escalas que califican esa calidad de forma cualitativa, cromáticas o numérica. Ejemplo  de  este  tipo  de  índices  es  el  Índice Metropolitano  de  Calidad  del  Aire,  IMECA, que  se  utiliza  en  la  Zona  Metropolitana  del Valle de México, ZMVM. [(1- Principios de Medición de la Calidad del Aire.pdf)]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Modo de cálculo\n",
    "\n",
    "- El Índice de Calidad del Aire se reportará regularmente cada hora, todos los días del año. El Índice de Calidad del Aire se calculará para cada uno de los contaminantes reportados en las Estaciones de Monitoreo continuo consideradas para el uso del algoritmo que integra el SIMAT. \n",
    " \n",
    "- El Índice de Calidad del Aire reportado por las Estaciones de Monitoreo consideradas para el uso del algoritmo, corresponderá al valor máximo estimado para el contaminante que registre la mayor concentración. Adicionalmente, se reportará el índice máximo obtenido por el SIMAT. \n",
    "\n",
    "Con base a estos criterios es que se llevo a cabo la predicción."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Alcance del análisis"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Alcaldía: Cuahtemoc\n",
    "\n",
    "Esto se traduce a las estaciones de medicion:\n",
    "- Cuahtémoc: HGM (Hospital General de México). Zona Centro de CDMX."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Contaminantes\n",
    "* PM10\n",
    "* PM2.5\n",
    "* O3"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
