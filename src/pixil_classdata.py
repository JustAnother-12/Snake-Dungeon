from typing import List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Colors:
    default: List[str]
    simple: List[str]
    common: List[str]
    skintones: List[str]

    def __init__(self, default: List[str], simple: List[str], common: List[str], skintones: List[str]) -> None:
        self.default = default
        self.simple = simple
        self.common = common
        self.skintones = skintones

    @staticmethod
    def from_dict(obj: Any) -> 'Colors':
        assert isinstance(obj, dict)
        default = from_list(from_str, obj.get("default"))
        simple = from_list(from_str, obj.get("simple"))
        common = from_list(from_str, obj.get("common"))
        skintones = from_list(from_str, obj.get("skin tones"))
        return Colors(default, simple, common, skintones)

    def to_dict(self) -> dict:
        result: dict = {}
        result["default"] = from_list(from_str, self.default)
        result["simple"] = from_list(from_str, self.simple)
        result["common"] = from_list(from_str, self.common)
        result["skin tones"] = from_list(from_str, self.skintones)
        return result


class Filter:
    brightness: str
    contrast: str
    grayscale: str
    blur: int
    huerotate: int
    dropshadowx: int
    dropshadowy: int
    dropshadowblur: int
    dropshadowalpha: int

    def __init__(self, brightness: str, contrast: str, grayscale: str, blur: int, huerotate: int, dropshadowx: int, dropshadowy: int, dropshadowblur: int, dropshadowalpha: int) -> None:
        self.brightness = brightness
        self.contrast = contrast
        self.grayscale = grayscale
        self.blur = blur
        self.huerotate = huerotate
        self.dropshadowx = dropshadowx
        self.dropshadowy = dropshadowy
        self.dropshadowblur = dropshadowblur
        self.dropshadowalpha = dropshadowalpha

    @staticmethod
    def from_dict(obj: Any) -> 'Filter':
        assert isinstance(obj, dict)
        brightness = from_str(obj.get("brightness"))
        contrast = from_str(obj.get("contrast"))
        grayscale = from_str(obj.get("grayscale"))
        blur = from_int(obj.get("blur"))
        huerotate = from_int(obj.get("hue-rotate"))
        dropshadowx = from_int(obj.get("dropshadow_x"))
        dropshadowy = from_int(obj.get("dropshadow_y"))
        dropshadowblur = from_int(obj.get("dropshadow_blur"))
        dropshadowalpha = from_int(obj.get("dropshadow_alpha"))
        return Filter(brightness, contrast, grayscale, blur, huerotate, dropshadowx, dropshadowy, dropshadowblur, dropshadowalpha)

    def to_dict(self) -> dict:
        result: dict = {}
        result["brightness"] = from_str(self.brightness)
        result["contrast"] = from_str(self.contrast)
        result["grayscale"] = from_str(self.grayscale)
        result["blur"] = from_int(self.blur)
        result["hue-rotate"] = from_int(self.huerotate)
        result["dropshadow_x"] = from_int(self.dropshadowx)
        result["dropshadow_y"] = from_int(self.dropshadowy)
        result["dropshadow_blur"] = from_int(self.dropshadowblur)
        result["dropshadow_alpha"] = from_int(self.dropshadowalpha)
        return result


class Options:
    blend: str
    locked: bool
    filter: Filter

    def __init__(self, blend: str, locked: bool, filter: Filter) -> None:
        self.blend = blend
        self.locked = locked
        self.filter = filter

    @staticmethod
    def from_dict(obj: Any) -> 'Options':
        assert isinstance(obj, dict)
        blend = from_str(obj.get("blend"))
        locked = from_bool(obj.get("locked"))
        filter = Filter.from_dict(obj.get("filter"))
        return Options(blend, locked, filter)

    def to_dict(self) -> dict:
        result: dict = {}
        result["blend"] = from_str(self.blend)
        result["locked"] = from_bool(self.locked)
        result["filter"] = to_class(Filter, self.filter)
        return result


class Layer:
    id: int
    src: str
    edit: bool
    name: str
    opacity: int
    active: bool
    unqid: str
    options: Options

    def __init__(self, id: int, src: str, edit: bool, name: str, opacity: int, active: bool, unqid: str, options: Options) -> None:
        self.id = id
        self.src = src
        self.edit = edit
        self.name = name
        self.opacity = opacity
        self.active = active
        self.unqid = unqid
        self.options = options

    @staticmethod
    def from_dict(obj: Any) -> 'Layer':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        src = from_str(obj.get("src"))
        edit = from_bool(obj.get("edit"))
        name = from_str(obj.get("name"))
        opacity = int(from_str(obj.get("opacity")))
        active = from_bool(obj.get("active"))
        unqid = from_str(obj.get("unqid"))
        options = Options.from_dict(obj.get("options"))
        return Layer(id, src, edit, name, opacity, active, unqid, options)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["src"] = from_str(self.src)
        result["edit"] = from_bool(self.edit)
        result["name"] = from_str(self.name)
        result["opacity"] = from_str(str(self.opacity))
        result["active"] = from_bool(self.active)
        result["unqid"] = from_str(self.unqid)
        result["options"] = to_class(Options, self.options)
        return result


class Frame:
    name: str
    speed: int
    layers: List[Layer]
    active: bool
    selectedLayer: int
    unqid: str
    preview: str
    width: int
    height: int

    def __init__(self, name: str, speed: int, layers: List[Layer], active: bool, selectedLayer: int, unqid: str, preview: str, width: int, height: int) -> None:
        self.name = name
        self.speed = speed
        self.layers = layers
        self.active = active
        self.selectedLayer = selectedLayer
        self.unqid = unqid
        self.preview = preview
        self.width = width
        self.height = height

    @staticmethod
    def from_dict(obj: Any) -> 'Frame':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        speed = from_int(obj.get("speed"))
        layers = from_list(Layer.from_dict, obj.get("layers"))
        active = from_bool(obj.get("active"))
        selectedLayer = from_int(obj.get("selectedLayer"))
        unqid = from_str(obj.get("unqid"))
        preview = from_str(obj.get("preview"))
        width = from_int(obj.get("width"))
        height = from_int(obj.get("height"))
        return Frame(name, speed, layers, active, selectedLayer, unqid, preview, width, height)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["speed"] = from_int(self.speed)
        result["layers"] = from_list(lambda x: to_class(Layer, x), self.layers)
        result["active"] = from_bool(self.active)
        result["selectedLayer"] = from_int(self.selectedLayer)
        result["unqid"] = from_str(self.unqid)
        result["preview"] = from_str(self.preview)
        result["width"] = from_int(self.width)
        result["height"] = from_int(self.height)
        return result


class PixilType:
    application: str
    type: str
    version: str
    website: str
    author: str
    contact: str
    width: int
    height: int
    colors: Colors
    colorSelected: str
    frames: List[Frame]
    currentFrame: int
    speed: int
    name: str
    preview: str
    previewApp: str
    arteditid: int
    paletteid: bool
    createdat: int
    updatedat: int
    id: int

    def __init__(self, application: str, type: str, version: str, website: str, author: str, contact: str, width: int, height: int, colors: Colors, colorSelected: str, frames: List[Frame], currentFrame: int, speed: int, name: str, preview: str, previewApp: str, arteditid: int, paletteid: bool, createdat: int, updatedat: int, id: int) -> None:
        self.application = application
        self.type = type
        self.version = version
        self.website = website
        self.author = author
        self.contact = contact
        self.width = width
        self.height = height
        self.colors = colors
        self.colorSelected = colorSelected
        self.frames = frames
        self.currentFrame = currentFrame
        self.speed = speed
        self.name = name
        self.preview = preview
        self.previewApp = previewApp
        self.arteditid = arteditid
        self.paletteid = paletteid
        self.createdat = createdat
        self.updatedat = updatedat
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> 'PixilType':
        assert isinstance(obj, dict)
        application = from_str(obj.get("application"))
        type = from_str(obj.get("type"))
        version = from_str(obj.get("version"))
        website = from_str(obj.get("website"))
        author = from_str(obj.get("author"))
        contact = from_str(obj.get("contact"))
        width = from_int(obj.get("width"))
        height = from_int(obj.get("height"))
        colors = Colors.from_dict(obj.get("colors"))
        colorSelected = from_str(obj.get("colorSelected"))
        frames = from_list(Frame.from_dict, obj.get("frames"))
        currentFrame = from_int(obj.get("currentFrame"))
        speed = from_int(obj.get("speed"))
        name = from_str(obj.get("name"))
        preview = from_str(obj.get("preview"))
        previewApp = from_str(obj.get("previewApp"))
        arteditid = from_int(obj.get("art_edit_id"))
        paletteid = from_bool(obj.get("palette_id"))
        createdat = from_int(obj.get("created_at"))
        updatedat = from_int(obj.get("updated_at"))
        id = from_int(obj.get("id"))
        return PixilType(application, type, version, website, author, contact, width, height, colors, colorSelected, frames, currentFrame, speed, name, preview, previewApp, arteditid, paletteid, createdat, updatedat, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["application"] = from_str(self.application)
        result["type"] = from_str(self.type)
        result["version"] = from_str(self.version)
        result["website"] = from_str(self.website)
        result["author"] = from_str(self.author)
        result["contact"] = from_str(self.contact)
        result["width"] = from_int(self.width)
        result["height"] = from_int(self.height)
        result["colors"] = to_class(Colors, self.colors)
        result["colorSelected"] = from_str(self.colorSelected)
        result["frames"] = from_list(lambda x: to_class(Frame, x), self.frames)
        result["currentFrame"] = from_int(self.currentFrame)
        result["speed"] = from_int(self.speed)
        result["name"] = from_str(self.name)
        result["preview"] = from_str(self.preview)
        result["previewApp"] = from_str(self.previewApp)
        result["art_edit_id"] = from_int(self.arteditid)
        result["palette_id"] = from_bool(self.paletteid)
        result["created_at"] = from_int(self.createdat)
        result["updated_at"] = from_int(self.updatedat)
        result["id"] = from_int(self.id)
        return result


def PixilTypefromdict(s: Any) -> PixilType:
    return PixilType.from_dict(s)


def PixilTypetodict(x: PixilType) -> Any:
    return to_class(PixilType, x)