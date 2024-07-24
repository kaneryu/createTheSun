from materialyoucolor.hct import Hct
from materialyoucolor.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot

from PySide6.QtCore import Qt, QObject, Slot



class Theme(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.primary_paletteKeyColor: str
        self.secondary_paletteKeyColor: str
        self.tertiary_paletteKeyColor: str
        self.neutral_paletteKeyColor: str
        self.neutral_variant_paletteKeyColor: str
        self.background: str
        self.onBackground: str
        self.surface: str
        self.surfaceDim: str
        self.surfaceBright: str
        self.surfaceContainerLowest: str
        self.surfaceContainerLow: str
        self.surfaceContainer: str
        self.surfaceContainerHigh: str
        self.surfaceContainerHighest: str
        self.onSurface: str
        self.surfaceVariant: str
        self.onSurfaceVariant: str
        self.inverseSurface: str
        self.inverseOnSurface: str
        self.outline: str
        self.outlineVariant: str
        self.shadow: str
        self.scrim: str
        self.surfaceTint: str
        self.primary: str
        self.onPrimary: str
        self.primaryContainer: str
        self.onPrimaryContainer: str
        self.inversePrimary: str
        self.secondary: str
        self.onSecondary: str
        self.secondaryContainer: str
        self.onSecondaryContainer: str
        self.tertiary: str
        self.onTertiary: str
        self.tertiaryContainer: str
        self.onTertiaryContainer: str
        self.error: str
        self.onError: str
        self.errorContainer: str
        self.onErrorContainer: str
        self.primaryFixed: str
        self.primaryFixedDim: str
        self.onPrimaryFixed: str
        self.onPrimaryFixedVariant: str
        self.secondaryFixed: str
        self.secondaryFixedDim: str
        self.onSecondaryFixed: str
        self.onSecondaryFixedVariant: str
        self.tertiaryFixed: str
        self.tertiaryFixedDim: str
        self.onTertiaryFixed: str
        self.onTertiaryFixedVariant: str

    @Slot(str, result=str)
    def getColor(self, color: str) -> str:
        """Get color from color name

        Args:
            color (str): Name of color

        Returns:
            str: Hex value of color
        """
        return getattr(self, color)
    
    def get_dynamicColors(self, source: int, dark: bool, contrast: float) -> SchemeTonalSpot:
        """Get dynamic colors from source color

        Args:
            source (int): HCT color in int form
            dark (bool): _description_
            contrast (float): _description_

        Returns:
            SchemeTonalSpot: _description_
        """
        scheme = SchemeTonalSpot( # choose any scheme here
            
            Hct.from_int(source), # source color in hct form
            dark, # dark mode
            contrast, # contrast
        )
        
        for color in vars(MaterialDynamicColors).keys():
            color_name = getattr(MaterialDynamicColors, color)
            if hasattr(color_name, "get_hct"): # is a color
                #print("self." + color + ": str")
                self.__setattr__(color, self.list_rgb_to_hex(color_name.get_hct(scheme).to_rgba())) # set attribute of color name to its value in rgba format

    def list_rgb_to_hex(self, color: list[int]) -> str:
        """Convert a list of rgb values to a hex string

        Args:
            color (list[int]): List of rgb values

        Returns:
            str: Hex string
        """
        return "#" + "".join([hex(x)[2:].zfill(2) for x in color[:3]]) # color[:3] because we don't need the alpha value