Model adjustment data format
============================



.. code-block:: python

   {
       'metadata': {
           'type': 'model-adjustment',
           'date': 'YYYY-MM-DDTHH:MM:SS+00:00',
           'version': version_tuple,
       },
       'distribution': {
           ...
       },
       'region': {
           ...
       },
       'diffraction': {
           ...
       },
       'profile': {
           'harmonic': harmonic,
           'part': 'real',
           'variable': [L0, L1, ...],
           'amplitude': [A_L0, A_L1, ...],
       },
       'limits': {
           'linear': i_Lmax_linear,
           'positive': i_Lmax_positive,
       },
       'adjustment': {
           'model': 'numlpa.kits.models.name',
           'optimizer': 'numlpa.kits.optimizers.name',
           'interval': 'linear',
           'variable': [L0, L1, ...],
           'amplitude': [A_L0, A_L1, ...],
           'deviation': std,
       },
       'parameters': {
           'parameter-1': value_1,
           'parameter-2': value_2,
           ...
       },
   }

Description of mandatory entries:

* ``metadata``: Section containing general information related to the nature of the data.

  * ``type``: Identifier associated with the data category.

  * ``date``: Date of data generation, in `ISO 8601 <https://www.iso.org/iso-8601-date-and-time-format.html>`_ standard.

  * ``version``: Version of NumLPA.

* ``distribution``: Section containing data related to the dislocation probability distribution.

  * See :doc:`dislocation sample data format <dislocation-sample>`.

* ``region``: Section containing data related to the region of interest.

  * See :doc:`dislocation sample data format <dislocation-sample>`.

* ``diffraction``:

  * See :doc:`Fourier transform data format <fourier-transform>`.

* ``coefficients``:

  * See :doc:`Fourier transform data format <fourier-transform>`.

* ``adjustment``:

  * ``model``:

  * ``filter``:

  * ``optimizer``:

  * ``harmonic``:

  * ``amplitudes``:

  * ``deviation``:

* ``parameters``:

  * Value of each optimal parameter, for each fitting range.
